#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : Arte - WoW
# -----------------------------------------------------------------------------
# Author : 
# -----------------------------------------------------------------------------
# License : proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 14-Jan-2014
# Last mod : 14-Jan-2014
# -----------------------------------------------------------------------------
from django.db import models
from django.utils.translation import ugettext as _
import inspect
import sys

# -----------------------------------------------------------------------------
# 
#     Choices field types
# 
# -----------------------------------------------------------------------------
class BaseChoiceField(models.Model):
    title = models.CharField(_('Title of this choice'), max_length=120)

class TextChoiceField(BaseChoiceField):
    pass

class MediaChoiceField(BaseChoiceField):
    pass

class ImageChoiceField(MediaChoiceField):
    pass

class IconChoiceField(MediaChoiceField):
    pass

# -----------------------------------------------------------------------------
# 
#     Typologies
# 
# -----------------------------------------------------------------------------
class TypologyManager(models.Manager):
    def create_typology(self, typology_type, question_id):
        typology = getattr(sys.modules[__name__], typology_type)
        question = Question.objects.get(pk=question_id)
        typology = typology(sub_type=typology_type, question=question)
        typology.save()
        return typology

class Typology(models.Model):
    sub_type = models.CharField(_('Typology subtype'), max_length=30)
    question = models.OneToOneField('Question')    
    objects  = TypologyManager()

class BaseMultipleChoicesTypology(Typology):
    choices = models.ManyToManyField('BaseChoiceField')

class SelectionTypology(BaseMultipleChoicesTypology):
    help_text = "Multiple choices question (1 or more answer)"
    # multiple choices allowed
    value = models.ManyToManyField('BaseChoiceField')

class RadioTypology(BaseMultipleChoicesTypology):
    help_text = "Radio choices question (1 answer only)"
    # single value

class NumberTypology(Typology): 
    help_text = "Number input field"
    unit = models.CharField(_('Number unit (e.g "%", "$", "kg")'), max_length=15)

class RangeNumberTypology(Typology):
    help_text = "Number inside a range typology"
    unit = models.CharField(_('Number unit (e.g "%", "$", "kg")'), max_length=15)
    min_number = models.PositiveIntegerField(default=0)
    max_number = models.PositiveIntegerField(default=100)

    def __unicode__(self):
        return "Range: [{min}, {max}] {unit}".format(
            min=self.min_number, max=self.max_number, unit=self.unit
        )

class BooleanTypology(RadioTypology):
    help_text = "Boolean choice question (1 answer only)"
    @classmethod
    def create(klass):
        choices  = (
            # default yes choice,
            TextChoiceField(title=_('yes')),
            TextChoiceField(title=_('no')),
            # default no choice
        )
        typology = klass()
        typology.choices += choices
        return typology

def list_typologies():
    """
    List all the class inherited from app.core.models.Typology
    """
    module     = __name__
    typologies = []
    for name, klass in inspect.getmembers(sys.modules[module], inspect.isclass):
        if Typology in inspect.getmro(klass) and klass is not Typology:
            typologies.append(klass)
    return typologies

TYPOLOGIES_TYPES = [(t.__name__, t.help_text) for t in list_typologies() if getattr(t, "help_text", None)]

# -----------------------------------------------------------------------------
#
#    Questions
#
# -----------------------------------------------------------------------------
class Question(models.Model):
    label         = models.CharField(_('Question label'), max_length=220)
    hint_text     = models.CharField(_('Question hint text'), max_length=120)
    typology_type = models.CharField(_('Question typology'), max_length=30, choices=TYPOLOGIES_TYPES)

    def save(self, *args, **kwargs):
        super(Question, self).save()
        if self.pk and self.typology_type:
            old = Typology.objects.filter(question_id=self.pk)
            for _t in old:
                _t.delete()

            Typology.objects.create_typology(
                typology_type=self.typology_type,
                question_id=self.pk
            )

# EOF
