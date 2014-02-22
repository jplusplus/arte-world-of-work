#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Project : Arte - WoW
# -----------------------------------------------------------------------------
# Author : Bellon Pierre                              <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# License : proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 14-Jan-2014
# Last mod : 15-Jan-2014
# -----------------------------------------------------------------------------
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import ImageField


class ThematicElementMixin(models.Model):
    """
    Inject generic_element to a model that has a representative ThematicElement
    """
    class Meta:
        abstract = True

    generic_element = generic.GenericRelation('ThematicElement')
        
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


class AsFinalMixin(models.Model):
    class Meta:
        abstract = True

    content_type = models.ForeignKey(ContentType, editable=False)
    content_object = generic.GenericForeignKey('content_type', 'pk')
    
    def as_final(self):
        return self.content_object


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


class ValidateButtonMixin(models.Model):
    class Meta:
        abstract = True
    validate_button_label = models.CharField(_('Validate button (label)'), default=_('Done'), max_length=120)