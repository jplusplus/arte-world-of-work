#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# License: GNU General Public License
# -----------------------------------------------------------------------------
# Creation time:      2014-03-21 15:05:09
# Last Modified time: 2014-04-10 12:24:10
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

from django import forms
from django.db import models as db_models 
from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes import generic
from sorl.thumbnail.admin import AdminImageMixin
from tinymce.widgets import TinyMCE

import sys

from app.core import models
# -----------------------------------------------------------------------------
#
#    Inlines
#
# -----------------------------------------------------------------------------
# Question related inlines 
class InlineQuestionMedia(admin.StackedInline):
    model = models.QuestionMediaAttachement
    extra = 0
    max_num = 1

class InlineTextSelectionQuestion(admin.StackedInline):
    model   = models.TextChoiceField
    extra   = 0
    max_num = 10

class InlineMediaSelectionQuestion(AdminImageMixin, admin.StackedInline):
    model   = models.MediaChoiceField
    extra   = 0
    max_num = 10

class InlineTextRadioQuestion(InlineTextSelectionQuestion):
    pass 

class InlineMediaRadioQuestion(InlineMediaSelectionQuestion):
    pass

class InlineBooleanQuestion(InlineTextRadioQuestion):
    pass

class InlineUserGenderQuestion(InlineTextRadioQuestion):
    model = models.UserChoiceField

class GenericInlineThematicElement(generic.GenericStackedInline):
    model = models.ThematicElement
    extra = 0
    max_num = 1

class InlineThematicElement(admin.TabularInline):
    model = models.ThematicElement
    readonly_fields = 'content_type', 'object_id'
    extra = 0
    max_num = 0

# -----------------------------------------------------------------------------
#
#    Question
#
# -----------------------------------------------------------------------------
class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ('content_type',)
    inlines = (
        InlineQuestionMedia,
        GenericInlineThematicElement,
    )

    def get_inline_instances(self, request, obj=None):
        """ Add a inline with the name Inline<QuestionClassName> if exists """
        inline_model_admins = super(QuestionAdmin, self).get_inline_instances(request, obj)
        if self.model:
            # return the related Inline class for the given question_type.
            # Inline class must have a name like Inline<QuestionClassName>
            inline = getattr(sys.modules[__name__], "Inline%s" % (self.model.__name__), None)
            if inline:
                inline = inline(self.model, self.admin_site)
                inline_model_admins.append(inline)
        return inline_model_admins


class ThematicAdmin(admin.ModelAdmin):    
    prepopulated_fields = {'slug': ('title',)}
    inlines = (
        InlineThematicElement,
    )



class FeedbackAdmin(admin.ModelAdmin):
    pass


class AnswerAdmin(admin.ModelAdmin): 
    readonly_fields = ('content_type',)


# -----------------------------------------------------------------------------
#
#    Register your models here
#
# -----------------------------------------------------------------------------
# all questions models 
admin.site.register(models.TypedNumberQuestion   , QuestionAdmin)

# admin.site.register(models.TextRadioQuestion    , QuestionAdmin)
# admin.site.register(models.TextSelectionQuestion, QuestionAdmin)

admin.site.register(models.MediaRadioQuestion    , QuestionAdmin)
admin.site.register(models.MediaSelectionQuestion, QuestionAdmin)
admin.site.register(models.BooleanQuestion       , QuestionAdmin)

admin.site.register(models.UserAgeQuestion       , QuestionAdmin)
admin.site.register(models.UserCountryQuestion   , QuestionAdmin)
admin.site.register(models.UserGenderQuestion    , QuestionAdmin)

admin.site.register(models.Thematic              , ThematicAdmin)

admin.site.register(models.StaticFeedback        , FeedbackAdmin)

# Disabled (for now)
if settings.DEBUG and False:
    admin.site.register(models.TypedNumberAnswer     , AnswerAdmin)
    admin.site.register(models.SelectionAnswer       , AnswerAdmin)
    admin.site.register(models.RadioAnswer           , AnswerAdmin)
    admin.site.register(models.BooleanAnswer         , AnswerAdmin)

# EOF
