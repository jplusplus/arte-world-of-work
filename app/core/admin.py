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
from django import forms
from django.contrib import admin
from django.contrib.admin import TabularInline, StackedInline
from app.core.models import Question, Typology, SelectionTypology
from app.core.models import NumberTypology, RangeNumberTypology

class TypologyInlineFactory(object):
    types = {}
    @classmethod
    def get_instance(kls, type, site):
        inline = kls.types[type]
        inline['instance'] = inline.get('instance', None) or inline['klass'](inline['model'], site)
        print "instance: %s " % inline['instance']
        return inline['instance']

    @classmethod
    def register_inline(klass, model, inline_klass):
        typology_type = model.__name__
        inline = {
            'klass': inline_klass,
            'model': model
        }
        # model "types: %s " % klass.types
        # print "%s: %s " % (typology_type,  inline)
        klass.types[typology_type] = inline

class TypologyAdminForm(forms.ModelForm):
    model = Typology

class NumberTypologyAdminForm(TypologyAdminForm):
    model = NumberTypology

class RangeNumberTypologyAdminForm(TypologyAdminForm):
    model = RangeNumberTypology

class InlineTypologyAdmin(TabularInline):
    exclude = ('sub_type','question',)
    form = TypologyAdminForm
    model = Typology

class InlineNumberTypologyAdmin(InlineTypologyAdmin):
    form = NumberTypologyAdminForm
    model = NumberTypology

class InlineRangeNumberTypologyAdmin(InlineTypologyAdmin):
    form = RangeNumberTypologyAdminForm
    model = RangeNumberTypology

TypologyInlineFactory.register_inline(NumberTypology, InlineNumberTypologyAdmin)
TypologyInlineFactory.register_inline(RangeNumberTypology, InlineRangeNumberTypologyAdmin)

class QuestionAdmin(admin.ModelAdmin):
    fields = ('label', 'hint_text', 'typology_type')
    # inlines = (
    #     # InlineNumberTypologyAdmin,
    #     InlineRangeNumberTypologyAdmin,
    # ) 
    def get_inline_instances(self, request, obj=None):

        typology_type = request.POST.get('typology_type') or None
        if not typology_type and obj != None and obj.typology_type:
            typology_type = obj.typology_type
        print "typology: %s " % typology_type
        if typology_type:
            return (
                TypologyInlineFactory.get_instance(typology_type, self.admin_site),
            )
        else:
            return list()

# Register your models here.
admin.site.register(Question, QuestionAdmin)

# EOF
