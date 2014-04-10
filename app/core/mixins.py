#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# License: GNU General Public License
# -----------------------------------------------------------------------------
# Creation time:      2014-03-21 15:04:04
# Last Modified time: 2014-04-10 12:24:26
# -----------------------------------------------------------------------------
# This file is part of World of Work
# 
#   World of Work is a study about european youth's perception of work
#   Copyright (C) 2014 Journalism++
#   
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#   
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <http://www.gnu.org/licenses/>.

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import ImageField
from app.core import types

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


class MediaTypeMixin(models.Model):
    """ 
    Special model mixin for MediaChoices (radio and selection)
    Will include media_type field to inherited classes
    """ 
    class Meta:
        abstract = True
    media_type = models.CharField(_('Choice\'s media type'), max_length=15, \
                    choices=types.MEDIA_TYPES, blank=True, null=True)