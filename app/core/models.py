#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Project : Arte - WoW
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 14-Jan-2014
# Last mod : 15-Jan-2014
# -----------------------------------------------------------------------------

from django.contrib.contenttypes import generic 
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models
from django.db.models.fields import FieldDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from sorl.thumbnail import ImageField
from app import utils 

# -----------------------------------------------------------------------------
#
#     Constants
# 
# -----------------------------------------------------------------------------
MEDIA_TYPES = (
    ('icon', _('Icon (small)')),
    ('image', _('Image (big)')),
)

GENDER_TYPES = (
    ('male', _('Male')),
    ('female', _('Female')),
)

# User profile 
class UserProfile(models.Model):
    user           = models.OneToOneField(settings.AUTH_USER_MODEL, unique=True)
    age            = models.PositiveIntegerField(null=True)
    native_country = CountryField(null=True)
    living_country = CountryField(null=True)
    gender         = models.CharField(_('User gender'), max_length=50, 
        choices=GENDER_TYPES, null=True)

class UserPosition(models.Model):
    user              = models.OneToOneField(settings.AUTH_USER_MODEL, unique=True)
    thematic_position = models.PositiveIntegerField(default=0, null=True, blank=True)
    element_position  = models.PositiveIntegerField(default=0, null=True, blank=True)

# -----------------------------------------------------------------------------
# 
#     Pictures & Inherithed models 
# 
# -----------------------------------------------------------------------------
class PictureMixin(models.Model):
    """
    Generic model for attached pictures (to question, choice or feedback)
    """
    class Meta:
        abstract = True
    picture = ImageField(upload_to='uploaded', null=True, blank=True)

class QuestionMediaAttachement(PictureMixin):
    """
    Attached picture for a question
    """
    question = models.OneToOneField('BaseQuestion')

class ValidateButtonMixin(models.Model):
    class Meta:
        abstract = True
    validate_button_label = models.CharField(_('Validate button (label)'), default=_('Done'), max_length=120)

# -----------------------------------------------------------------------------
# 
#     Thematics
# 
# -----------------------------------------------------------------------------
# generic element for thematic, shall be questions or feedback
class ThematicElement(models.Model):
    class Meta:
        ordering= ['position']

    content_type   = models.ForeignKey(ContentType)
    object_id      = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    thematic = models.ForeignKey('Thematic', null=True, blank=True)
    position = models.PositiveIntegerField(null=True, blank=True)

    def _get_type(self):
        type = None
        model_klass = self.content_type.model_class()
        if issubclass(model_klass, BaseQuestion):
            type = 'question'
        elif issubclass(model_klass, BaseFeedback):
            type = 'feedback'
        return type

    # properties         
    type = property(_get_type)

    def __unicode__(self):
        return u"{type} - {title}".format(
            type=self.content_type,
            title=str(self.content_object)
        )

class ThematicElementMixin(models.Model):
    """
    Inject generic_element to a model that has a representative ThematicElement
    """
    class Meta:
        abstract = True

    generic_element = generic.GenericRelation(ThematicElement)
        
    def as_element(self):
        ctype = ContentType.objects.get_for_model(self)
        elements = self.generic_element.filter(content_type=ctype, object_id=self.pk)
        if len(elements) > 0:
            return elements[0]
        else: 
            return None

    def set_thematic(self, thematic, position=None):
        element = self.as_element()
        element.thematic = thematic
        if position != None:
            element.position = position
        element.save()

class ThematicManager(models.Manager):
    def all_elements(self):
        thematics = self.get_queryset()
        elements = []
        for t in thematics: 
            elements += t.all_elements()
        return elements


class Thematic(models.Model):
    class Meta:
        ordering = ('position',)

    position = models.PositiveIntegerField(default=0)
    title = models.CharField(_('Thematic title'), max_length=120)
    elements = generic.GenericRelation(ThematicElement)
    objects = ThematicManager()

    intro_description = models.TextField(_('Introduction description'))
    intro_button_label = models.CharField(_('Introduction button label'), 
        default=_('See the data'), max_length=120, null=True, blank=True)


    def add_element(self, instance, position=None):
        # Add an element to a thematic object 
        # will convert passed concrete model `instance`, if instance doe
        assert issubclass(instance.__class__, ThematicElementMixin)
        element = instance.as_element() # can raise NotImplementedError 
        element.thematic = self
        if position != None:
            element.position = position
        element.save()

    def __unicode__(self):
        return u"{id} - {title}".format(id=self.pk, title=self.title)

    def all_elements(self):
        # list all elements (feedback + question) of a thematic object
        final_elements = []
        for element in self.thematicelement_set.all():
            final_element = element.content_object
            final_element.position = element.position
            final_element.thematic = element.thematic
            # to keep original order we insert at the begining of the list
            final_elements.append(final_element)
        return final_elements

# -----------------------------------------------------------------------------
# 
#     Feedbacks
# 
# -----------------------------------------------------------------------------
class BaseFeedback(ValidateButtonMixin):
    content_type  = models.ForeignKey(ContentType, editable=False)
    html_sentence = models.CharField(_('Feedbacks sentence'), max_length=120, 
        help_text=_('Sentence (as html content): "Hey did you knew .. ?"')
    )
    # properties
    @property 
    def sub_type(self):
        klass = self.content_type.model_class().__name__
        klass = klass.replace('Feedback', '') # remove Question from klass name 
        return utils.camel_to_underscore(klass)

    def __unicode__(self):
        return 'Feedback: %s' % self.html_sentence[:60]

class StaticFeedback(BaseFeedback, ThematicElementMixin, PictureMixin):
    source_url = models.URLField()
    source_title = models.CharField(max_length=120)
    def __unicode__(self):
        return 'StaticFeedback: %s' % self.html_sentence[:60]



# -----------------------------------------------------------------------------
# 
#     Answer types
# 
# -----------------------------------------------------------------------------
class AnswerManager(models.Manager):
    def create_answer(self, question, user, value):
        answer_type =  question.answer_type
        answer = answer_type(question=question, user=user)
        field  = answer._meta.get_field('value')
        # check if value field is ManyToMany, ForeignKey or other
        if isinstance(field, models.ManyToManyField):
            # we must save answer object before adding related values
            answer.save()
            # if value is a single field object we need to wrap it in a list
            if isinstance(value, models.Model):
                value = (value,)
            for val in value:
                answer.value.add(val)
        else:
            if isinstance(value, UserChoiceField):
                # if answered value is an User choice we need to check for its 
                # inner value attribute or its title if value is `None`
                value = value.value or value.title 
            answer.value = value
        answer.save()
        return answer



class ResultManager(models.Manager):

    def all(self, question=None, gender=None, age_min=None, age_max=None):
        qs = self.get_queryset(question=question, gender=gender, age_min=age_min, age_max=age_max)
        return qs

    def get_queryset(self, question=None, gender=None, age_min=None, age_max=None):
        assert question != None, "ResultManager need a question to get your results"
        qs = super(ResultManager, self).get_queryset().filter(question=question)
        if gender != None:
            assert gender in map(lambda x:x[0], GENDER_TYPES), ("The given gender ",
                "({gender}) is not recognized as a valid gender.".format(gender=gender))

            qs = qs.filter(user__profile__gender=gender)

        if age_min and age_max:
            qs = qs.filter(user__profile__age__lte=age_max, user__profile__age__gte=age_min)
        return qs


class BaseAnswer(models.Model):
    content_type = models.ForeignKey(ContentType, editable=False)
    content_object = generic.GenericForeignKey('content_type', 'pk')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    question = models.ForeignKey('BaseQuestion')
    objects = AnswerManager()
    results = ResultManager()





class TypedNumberAnswer(BaseAnswer):
    value = models.IntegerField()

    def clean(self, *args, **kwargs):
        question = TypedNumberQuestion.objects.get(pk=self.question.pk)
        if self.value:
            if self.value < question.min_number:
                raise ValidationError('Answer is out of range: inferior to min_number')
            if self.value > question.max_number: 
                raise ValidationError('Answer is out of range: superior to max_number')

class SelectionAnswer(BaseAnswer):
    value = models.ManyToManyField('BaseChoiceField')

class RadioAnswer(BaseAnswer):
    value = models.ForeignKey('BaseChoiceField')

class UserProfileAnswer(BaseAnswer):
    """
    Base class for user answers. Its default behavior is to update
    a related field in a user profile (for this answer's user).
    """
    def get_profile_attribute(self): 
        # try to get field from meta // dynamic value
        try:
            profile_attribute = self.question.profile_attribute
        except FieldDoesNotExist:
            profile_attribute = self.question.__class__.profile_attribute
        return profile_attribute

    def save(self, *args, **kwargs):
        # get user profile
        profile = UserProfile.objects.get(user=self.user)
        profile_attribute = self.get_profile_attribute()
        setattr(profile, profile_attribute, self.value)
        profile.save()
        super(UserProfileAnswer, self).save(*args, **kwargs)

class UserCountryAnswer(UserProfileAnswer):
    value = CountryField()

class UserAgeAnswer(UserProfileAnswer):
    value = models.PositiveIntegerField()

class UserGenderAnswer(UserProfileAnswer):
    value = models.CharField(_('User gender'), max_length=50, choices=GENDER_TYPES)
# -----------------------------------------------------------------------------
#
#    Questions
#
# -----------------------------------------------------------------------------
class QuestionManager(models.Manager):
    def get_final_question(self, pk):
        base_question = self.get(id=pk)
        return base_question.as_final()

class BaseQuestion(ThematicElementMixin):
    """
    Base class for question, will be inherited by concrete question typologies
    """
    answer_type       = None
    label             = models.CharField(_('Question label')    , max_length=220)
    hint_text         = models.CharField(_('Question hint text'), max_length=120)
    content_type      = models.ForeignKey(ContentType, editable=False)
    skip_button_label = models.CharField(_('Skip button (label)'), default=_('Skip this question'),max_length=120)
    objects = QuestionManager()
    # properties 
    @property
    def typology(self):
        klass = self.content_type.model_class().__name__
        klass = klass.replace('Question', '') # remove Question from klass name 
        return utils.camel_to_underscore(klass)

    def __unicode__(self):
        return self.label[:25]

    def choices(self):
        return self.basechoicefield_set.all()

    def create_answer(self, *args, **kwargs):
        # we pass to `create_answer` method the related question 
        # (`kwargs['question']` or `self`
        kwargs['question'] = kwargs.get('question', self)
        return BaseAnswer.objects.create_answer(*args, **kwargs)

    def as_final(self):
        final_klass = self.content_type.model_class()
        return final_klass.objects.get(id=self.pk)

    @property
    def results(self, gender=None, age_min=0, age_max=100):
        return BaseAnswer.results.all(question=self, gender=gender, age_min=age_min, age_max=age_max )


    
class TypedNumberQuestion(BaseQuestion, ValidateButtonMixin):
    """
    TypedNumber question are questions where we ask user to select a number
    defined insided an interval.
    """
    class Meta:
        verbose_name = _('Number choice question')
        verbose_name_plural = _('Number choice questions')
    answer_type = TypedNumberAnswer
    unit = models.CharField(_('Number unit'), help_text=_('Unit that will be displayed after the min and max numbers.'), max_length=15)
    min_number = models.PositiveIntegerField(default=0)
    max_number = models.PositiveIntegerField(default=100)

# -----------------------------------------------------------------------------
#
#   Single (radio) & multiple (selection) possible answer questions  
#
# -----------------------------------------------------------------------------
class RadioQuestionMixin(BaseQuestion):
    """
    Mixin for radio question (one single answer)
    """ 
    class Meta:
        abstract = True
    answer_type = RadioAnswer

class SelectionQuestionMixin(BaseQuestion, ValidateButtonMixin):
    """ 
    Mixin for selection question (one on more answer)
    """
    class Meta:
        abstract = True
    answer_type = SelectionAnswer


class TextSelectionQuestion(SelectionQuestionMixin):
    """ Multiple Choices (text) question - one or more answer """
    class Meta:
        verbose_name = _('Text (multiple choices) question')
        verbose_name_plural = _('Text (multiple choices) questions')

class TextRadioQuestion(RadioQuestionMixin):
    """ Multiple Choice (text) question - single answer """
    class Meta:
        verbose_name = _('Text (single choice) question')
        verbose_name_plural = _('Text (single choice) questions')

class BooleanQuestion(RadioQuestionMixin):
    """ yes or no question - single answer """
    pass

class MediaTypeMixin(models.Model):
    """ 
    Special model mixin for MediaChoices (radio and selection)
    Will include media_type field to inherited classes
    """ 
    class Meta:
        abstract = True
    media_type = models.CharField(_('Choice\'s media type'), max_length=15, \
                    choices=MEDIA_TYPES)

class MediaRadioQuestion(RadioQuestionMixin, MediaTypeMixin):
    """ 
    Multiple Choice (image or icon) question - single answer. 

    Inherit from :model:`app.core.models.MediaTypeMixin`, thus inherit from its 
    `media_type` model's field.
    """
    class Meta:
        verbose_name = _('Media (single choice) question')
        verbose_name_plural = _('Media (single choice) questions')

class MediaSelectionQuestion(SelectionQuestionMixin, MediaTypeMixin):
    """ 
    Multiple Choice (image or icon) question - multiple answer. 

    Inherit from :model:`app.core.models.MediaTypeMixin`, thus inherit from its 
    `media_type` model's field.
    """
    class Meta:
        verbose_name = _('Media (multiple choices) question')
        verbose_name_plural = _('Media (multiple choices) questions')

# -----------------------------------------------------------------------------
# 
#     User specific questions
# 
# -----------------------------------------------------------------------------
class UserProfileQuestion(BaseQuestion):
    profile_attribute = None
    answer_type       = UserProfileAnswer

class UserAgeQuestion(UserProfileQuestion, ValidateButtonMixin):
    profile_attribute = 'age'
    answer_type       = UserAgeAnswer

class UserCountryQuestion(UserProfileQuestion):
    answer_type       = UserCountryAnswer
    # will lookup every CountryField attribute from UserProfile model
    profile_attribute = models.CharField(_('Related profile attribute'), max_length=20, 
        choices=[ ( name, name) for name in utils.get_fields_names(type=CountryField, model=UserProfile)],
        help_text=_('Select user profile attribute that will be changed by user answer'), null=True)

class UserGenderQuestion(UserProfileQuestion):
    profile_attribute = 'gender'
    answer_type = UserGenderAnswer

# -----------------------------------------------------------------------------
# 
#     Choices field types
# 
# -----------------------------------------------------------------------------
class BaseChoiceField(models.Model):
    """
    Base class for choices, will be inherited by concrete choices (text and 
    media)
    """
    content_type = models.ForeignKey(ContentType, editable=False)
    content_object = generic.GenericForeignKey('content_type', 'pk')
    question = models.ForeignKey('BaseQuestion')
    title = models.CharField(_('Title of this choice'), max_length=120)

class TextChoiceField(BaseChoiceField):
    pass

class MediaChoiceField(BaseChoiceField, PictureMixin):
    pass

class UserChoiceField(BaseChoiceField):
    value = models.CharField(_('Value of this field'), blank=True, 
        null=True, max_length=120, help_text=_('It will tell user model what \
        value should be stored in related field'))

# trigger signals binding 
import signals; signals.bind()