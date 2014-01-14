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

    def create_typology(self, typology_type):
        typology = getattr(sys.modules[__name__], typology_type)
        typology = typology()
        typology.save()
        return typology

class Typology(models.Model):
    sub_type = models.CharField(_('Typology subtype'), max_length=30)
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
    value = models.ForeignKey(BaseChoiceField)

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

# -----------------------------------------------------------------------------
#
#    Questions
#
# -----------------------------------------------------------------------------
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

class Question(models.Model):
    label         = models.CharField(_('Question label'), max_length=220)
    hint_text     = models.CharField(_('Question hint text'), max_length=120)
    typology_type = models.CharField(_('Question typology'), max_length=30, choices=TYPOLOGIES_TYPES)
    typology      = models.OneToOneField(Typology, primary_key=True)

    def save(self, *args, **kwargs):
        if self.typology_type:
            self.typology = Typology.objects.create_typology(self.typology_type)
        super(Question, self).save()

# EOF
