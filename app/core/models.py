#!/usr/bin/env python
# Encoding: utf-8
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
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext as _

from django_countries.fields import CountryField
from sorl.thumbnail import ImageField

# -----------------------------------------------------------------------------
#
#     Constants
# 
# -----------------------------------------------------------------------------
MEDIA_TYPES = (
    ('icon', _('Icon (small)')),
    ('image', _('Image (big)')),
)
# User profile 
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    age = models.PositiveIntegerField(null=True)
    country = CountryField(null=True)

# -----------------------------------------------------------------------------
# 
#     Answer types
# 
# -----------------------------------------------------------------------------
class AnswerManager(models.Manager):
    def create_answer(self, question, user, value):
        answer_type =  question.answer_type
        answer = answer_type(question=question, user=user)

        # import pdb; pdb.set_trace()
        # check if value field is ManyToMany, ForeignKey or other
        if 'value' in [(f.name) for f in answer._meta.many_to_many]:
            answer.save()
            for val in value:
                answer.value.add(val)
        else:
            answer.value = value
        return answer

class BaseAnswer(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey('BaseQuestion', unique=True)
    objects = AnswerManager()

class CountryAnswer(BaseAnswer):
    value = CountryField()

class NumberAnswer(BaseAnswer):
    value = models.IntegerField()

class TypedNumberAnswer(NumberAnswer):
    def clean(self):
        question = TypedNumberQuestion.objects.get(pk=self.question_id)
        if self.value:
            if self.value < question.min_number:
                raise ValidationError('Answer is out of range: inferior to min_number')
            if self.value > question.max_number: 
                raise ValidationError('Answer is out of range: superior to max_number')

class DateAnswer(BaseAnswer):
    value = models.DateTimeField()

class SelectionAnswer(BaseAnswer):
    value = models.ManyToManyField('BaseChoiceField')

class RadioAnswer(BaseAnswer):
    value = models.ForeignKey('BaseChoiceField')

class UserProfileAnswer(BaseAnswer):

    """
    Base class for user answers. Its default behavior is to update
    a related field in a user profile (for this answer's user).
    """

    def save(self, *args, **kwargs):
        # get user profile
        profile       = UserProfile.objects.get(user=self.user)
        profile_field = self.question.__class__.profile_attribute
        setattr(profile, profile_field, self.value)
        profile.save()

        super(UserProfileAnswer, self).save(*args, **kwargs)

class UserCountryAnswer(UserProfileAnswer):
    value = CountryField()

class UserAgeAnswer(UserProfileAnswer):
    value = models.PositiveIntegerField()
# -----------------------------------------------------------------------------
#
#    Questions
#
# -----------------------------------------------------------------------------
class QuestionManager(models.Manager):
    def all_questions(self):
        """ Rerturn all the question in the right and final type """
        # FIXME: should return a QuerySet, not a list
        generic_questions = super(QuestionManager, self).all()
        questions = []
        for q in generic_questions:
            final_class = q.content_type.model_class()
            # if it's a child of BaseQuestion
            if "basequestion_ptr" in final_class.__dict__.keys():
                q = final_class.objects.get(basequestion_ptr=q.id)
            questions.append(q)
        return questions


class BaseQuestion(models.Model):
    """
    Base class for question, will be inherited by concrete question typologies
    """
    answer_type  = None
    label        = models.CharField(_('Question label')    , max_length=220)
    hint_text    = models.CharField(_('Question hint text'), max_length=120)
    content_type = models.ForeignKey(ContentType, editable=False)
    # Managers
    objects = QuestionManager()

    def save(self, *args, **kwargs):
        self.content_type = ContentType.objects.get_for_model(self)
        super(BaseQuestion, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{type}: {label}".format(type=self.content_type, label=self.label[:25])

class UserProfileQuestion(BaseQuestion):
    profile_attribute = None
    answer_type       = UserProfileAnswer

class UserAgeQuestion(UserProfileQuestion):
    profile_attribute = 'age'
    answer_type       = UserAgeAnswer


class UserCountryQuestion(UserProfileQuestion):
    profile_attribute = 'country'
    answer_type       = UserCountryAnswer

class PictureMixin(models.Model):
    """
    Mixin for attached pictures (to question or choice)
    """
    class Meta:
        abstract = True 
    picture = ImageField(upload_to='uploaded')

    
class NumberQuestion(BaseQuestion):
    """
    Number question are designed for age and other types of questions where 
    we ask user to enter a 2 digit number
    """
    answer_type = NumberAnswer

class TypedNumberQuestion(BaseQuestion):
    """
    TypedNumber question are questions where we ask user to select a number
    defined insided an interval.
    """
    answer_type = TypedNumberAnswer
    unit = models.CharField(_('Number type'), help_text=_('Unit that will be displayed after the min and max numbers.'), max_length=15)
    min_number = models.PositiveIntegerField(default=0)
    max_number = models.PositiveIntegerField(default=100)

class DateQuestion(BaseQuestion):
    """ Use it when you want to ask a date to user """ 
    answer_type = DateAnswer

class CountryQuestion(BaseQuestion):
    """ Question designed to let user select between a list of countries """ 
    answer_type = CountryAnswer

# -----------------------------------------------------------------------------
# 
#   Question attachments
# 
# -----------------------------------------------------------------------------
class QuestionPicture(PictureMixin):
    """
    Attached picture for a question
    """
    question = models.OneToOneField('BaseQuestion')


# -----------------------------------------------------------------------------
#
#   Single (radio) & multiple (selection) possible answer questions  
#
# -----------------------------------------------------------------------------

class MediaTypeMixin(models.Model):
    """ 
    Special model mixin for MediaChoices (radio and selection)
    Will include media_type field to inherited classes
    """ 
    class Meta:
        abstract = True
    media_type = models.CharField(_('Choice\'s media type'), max_length=15, \
                    choices=MEDIA_TYPES)

class RadioQuestionMixin(BaseQuestion):
    """
    Mixin for radio question (one single answer)
    """ 
    class Meta:
        abstract = True
    answer_type = RadioAnswer

class SelectionQuestionMixin(BaseQuestion):
    """ 
    Mixin for selection question (one on more answer)
    """
    class Meta:
        abstract = True
    answer_type = SelectionAnswer

class TextSelectionQuestion(SelectionQuestionMixin):
    """ Multiple Choices (text) question - one or more answer """
    pass

class TextRadioQuestion(RadioQuestionMixin):
    """ Multiple Choice (text) question - single answer """
    pass 

class MediaSelectionQuestion(SelectionQuestionMixin, MediaTypeMixin):
    """ 
    Multiple Choices (image or icon) question - one or more answer. 

    Inherit from :model:`app.core.models.MediaTypeMixin`, thus inherit from its 
    `media_type` model's field.
    """
    pass

class MediaRadioQuestion(RadioQuestionMixin, MediaTypeMixin):
    """ 
    Multiple Choice (image or icon) question - single answer. 

    Inherit from :model:`app.core.models.MediaTypeMixin`, thus inherit from its 
    `media_type` model's field.
    """
    pass

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
    question = models.ForeignKey('BaseQuestion')
    title = models.CharField(_('Title of this choice'), max_length=120)

class TextChoiceField(BaseChoiceField):
    pass

class MediaChoiceField(BaseChoiceField, PictureMixin):
    pass

# EOF
