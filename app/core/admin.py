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
from django.contrib import admin
import app.core.models as models
import sys

# -----------------------------------------------------------------------------
#
#    Question
#
# -----------------------------------------------------------------------------
class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ('content_type',)

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

# -----------------------------------------------------------------------------
#
#    Inlines
#
# -----------------------------------------------------------------------------
class InlineMultipleTextChoicesQuestion(admin.StackedInline):
    model   = models.TextChoiceField
    extra   = 0
    max_num = 10

# -----------------------------------------------------------------------------
#
#    Register your models here
#
# -----------------------------------------------------------------------------
admin.site.register(models.BaseQuestion               , QuestionAdmin)
admin.site.register(models.RangeNumberQuestion        , QuestionAdmin)
admin.site.register(models.MultipleTextChoicesQuestion, QuestionAdmin)

# EOF
