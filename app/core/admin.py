#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes import generic
from sorl.thumbnail.admin import AdminImageMixin
from app.core import models

import sys

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
    inlines = (
        GenericInlineThematicElement,
    )

class AnswerAdmin(admin.ModelAdmin): 
    readonly_fields = ('content_type',)


# -----------------------------------------------------------------------------
#
#    Register your models here
#
# -----------------------------------------------------------------------------
# all questions models 
admin.site.register(models.TypedNumberQuestion   , QuestionAdmin)
admin.site.register(models.TextSelectionQuestion , QuestionAdmin)
admin.site.register(models.TextRadioQuestion     , QuestionAdmin)
admin.site.register(models.MediaRadioQuestion    , QuestionAdmin)
admin.site.register(models.MediaSelectionQuestion, QuestionAdmin)
admin.site.register(models.BooleanQuestion       , QuestionAdmin)

admin.site.register(models.UserAgeQuestion       , QuestionAdmin)
admin.site.register(models.UserCountryQuestion   , QuestionAdmin)
admin.site.register(models.UserGenderQuestion    , QuestionAdmin)

admin.site.register(models.Thematic              , ThematicAdmin)

admin.site.register(models.StaticFeedback        , FeedbackAdmin)

if settings.DEBUG:
    admin.site.register(models.TypedNumberAnswer     , AnswerAdmin)
    admin.site.register(models.SelectionAnswer       , AnswerAdmin)
    admin.site.register(models.RadioAnswer           , AnswerAdmin)
    admin.site.register(models.BooleanAnswer         , AnswerAdmin)

# EOF
