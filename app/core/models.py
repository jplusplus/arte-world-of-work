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

import re

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

    def inject_types(self, types):
        self.types = types

    def type_from_klass(self, kls): 
        return re.sub( '(?<!^)(?=[A-Z])', '_', kls.__name__).lower()

    def klass_from_type(self, type):
        assert self.is_typology_type(type)
        return eval("".join(
                map(
                    lambda x: x.capitalize(),
                    type.split('_')
                )
            )
        )

    def is_typology_type(self, type):
        is_safe_name = len(re.findall('[\W]', type)) == 0
        is_in_subtypes = filter(lambda x: x[0] == type, self.types) is not None 
        return is_in_subtypes and is_safe_name

    def create_typology(self, type=None, question_id=None):
        print "question %s" % question_id
        typology_klass = self.klass_from_type(type)
        # import pdb; pdb.set_trace()
        question = Question.objects.get(pk=question_id)
        typology = typology_klass(sub_type=type, question=question)
        typology.save()
        return typology

class Typology(models.Model):
    sub_type = models.CharField(_('Typology subtype'), max_length=30)
    question = models.ForeignKey('Question')
    objects = TypologyManager()

    def get_subclass(self):
        return self.objects.klass_from_type(self.sub_type)


class BaseMultipleChoicesTypology(Typology):
    choices = models.ManyToManyField('BaseChoiceField')

class SelectionTypology(BaseMultipleChoicesTypology):
    # multiple choices allowed
    value = models.ManyToManyField('BaseChoiceField')

class RadioTypology(BaseMultipleChoicesTypology):
    # single value 
    value = models.ForeignKey(BaseChoiceField)

class BooleanTypology(RadioTypology):
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


TYPOLOGIES_TYPES = (
    ( Typology.objects.type_from_klass(SelectionTypology), _('Multiple choices question (1 or more answer)')),
    ( Typology.objects.type_from_klass(RadioTypology),     _('Radio choices question (1 answer only)'      )),
    ( Typology.objects.type_from_klass(BooleanTypology),   _('Boolean choice question (1 answer only)'     ))
)

Typology.objects.inject_types(TYPOLOGIES_TYPES)

class Question(models.Model):
    label = models.CharField(_('Question label'), max_length=220)
    hint_text = models.CharField(_('Question hint text'), max_length=120)
    typology_type = models.CharField(_('Question typology'), max_length=30, choices=TYPOLOGIES_TYPES)

    def save(self, *args, **kwargs):
        super(Question, self).save()
        if self.pk and self.typology_type:
            Typology.objects.create_typology(
                type=self.typology_type,
                question_id=self.pk
            )

