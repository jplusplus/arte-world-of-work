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
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django_countries.fields import CountryField

from sorl.thumbnail import ImageField

MEDIA_TYPES = (
    ('icon', _('Icon (small)')),
    ('image', _('Image (big)')),
)

# -----------------------------------------------------------------------------
# 
#     Answer types
# 
# -----------------------------------------------------------------------------
class BaseAnswer(models.Model):
    class Meta:
        abstract = True
    user = models.ForeignKey(User)
    question = models.ForeignKey('BaseQuestion')

class CountryAnswer(BaseAnswer):
    value = CountryField()

class NumberAnswer(BaseAnswer):
    value = models.IntegerField()

class DateAnswer(BaseAnswer):
    value = models.DateTimeField()

class SelectionAnswer(BaseAnswer):
    value = models.ManyToManyField('BaseChoiceField')

class RadioAnswer(BaseAnswer):
    value = models.ForeignKey('BaseChoiceField')

# -----------------------------------------------------------------------------
#
#    Questions Manager
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

class BaseMedia(models.Model):
    class Meta:
        abstract = True 
    picture = ImageField(upload_to='/uploaded')

class QuestionMedia(BaseMedia):
    question = models.OneToOneField('BaseQuestion')

# -----------------------------------------------------------------------------
#
#    Generic Question
#
# -----------------------------------------------------------------------------
class BaseQuestion(models.Model):
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

# -----------------------------------------------------------------------------
#
#    Question: Number
#
# -----------------------------------------------------------------------------
class NumberQuestion(BaseQuestion):
    answer_type = NumberAnswer
    unit = models.CharField(_('Number unit (e.g "%", "$", "kg")'), max_length=15)

# -----------------------------------------------------------------------------
#
#    Question: Range Number
#
# -----------------------------------------------------------------------------
class RangeNumberQuestion(BaseQuestion):
    answer_type = NumberAnswer
    unit = models.CharField(_('Number unit (e.g "%", "$", "kg")'), max_length=15)
    min_number = models.PositiveIntegerField(default=0)
    max_number = models.PositiveIntegerField(default=100)

class DateQuestion(BaseQuestion):
    answer_type = DateAnswer

class CountryQuestion(BaseQuestion):
    answer_type = CountryAnswer

# -----------------------------------------------------------------------------
#
#    Question: Multiple & single choice
#
# -----------------------------------------------------------------------------
class MediaTypeMixin(models.Model):
    # special model mixin for MediaChoices (radio and selection) 
    class Meta:
        abstract = True
    media_type = models.CharField(_('Type of attached media'), max_length=15, \
                    choices=MEDIA_TYPES)

class SelectionQuestionMixin(BaseQuestion):
    class Meta:
        abstract = True
    answer_type = SelectionAnswer
    
class RadioQuestionMixin(BaseQuestion):
    class Meta:
        abstract = True
    answer_type = RadioAnswer

# multiple text choices 
class TextSelectionQuestion(SelectionQuestionMixin):
    pass

# multiple media choices
class MediaSelectionQuestion(SelectionQuestionMixin, MediaTypeMixin):
    pass

class TextRadioQuestion(RadioQuestionMixin):
    pass 

class MediaRadioQuestion(RadioQuestionMixin, MediaTypeMixin):
    pass

# -----------------------------------------------------------------------------
# 
#     Choices field types
# 
# -----------------------------------------------------------------------------
class BaseChoiceField(models.Model):
    question = models.ForeignKey('BaseQuestion')
    title = models.CharField(_('Title of this choice'), max_length=120)

class TextChoiceField(BaseChoiceField):
    pass

class MediaChoiceField(BaseChoiceField, BaseMedia):
    pass

# EOF
