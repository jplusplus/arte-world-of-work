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
from django.contrib.contenttypes.models import ContentType

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

# -----------------------------------------------------------------------------
#
#    Generic Question
#
# -----------------------------------------------------------------------------
class BaseQuestion(models.Model):
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
#    Question: Range Number
#
# -----------------------------------------------------------------------------
class RangeNumberQuestion(BaseQuestion):
    unit = models.CharField(_('Number unit (e.g "%", "$", "kg")'), max_length=15)
    min_number = models.PositiveIntegerField(default=0)
    max_number = models.PositiveIntegerField(default=100)

# -----------------------------------------------------------------------------
#
#    Question: Multiple Text Choice
#
# -----------------------------------------------------------------------------
class MultipleTextChoicesQuestion(BaseQuestion):
    pass

# -----------------------------------------------------------------------------
# 
#     Choices field types
# 
# -----------------------------------------------------------------------------
class BaseChoiceField(models.Model):
    question = models.ForeignKey('BaseQuestion')

class TextChoiceField(BaseChoiceField):
    title = models.CharField(_('Title of this choice'), max_length=120)

# EOF
