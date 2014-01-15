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
    def get_instance(kls, type, related_model, site):
        try:
            inline = kls.types[type]
            inline['instance'] = inline['instance'] or inline['klass'](related_model, site)
            print "instance: %s " % inline['instance']
            return inline['instance']
        except KeyError:
            msg = """
                {typology} typology has not been registred, please register it 
                using `{klass}.register_inline()` method
                """.format(typology=type, klass=kls.__name__)
            raise Exception(msg)


    @classmethod
    def register_inline(klass, model, inline_klass):
        typology_type = model.__name__
        klass.types[typology_type] = { 
            'klass': inline_klass,
            'instance': None
        }

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

    def __unicode__(self):
        return self.__name__ 

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

    def get_inline_instances(self, request, obj=None):
        # dynamic inline instanciation, the following conditions are set to enable 
        # this feature, they are here to verify that: 
        # - we are not adding one question
        # - we are not editing one existing question's typology_type 
        inline_instances = super(QuestionAdmin, self).get_inline_instances(request, obj)
        typology_type = request.POST.get('typology_type', None)
        if not typology_type and obj != None and obj.typology_type and obj.pk:
            typology_type = obj.typology_type

        # If we are saving changes for existing question with a changed 
        # typology_type we shouldn't instantiate any new Inline because it 
        # will not relect the posted data and will produce a `ValidationError` 
        if typology_type and obj and obj.typology_type == typology_type:
            inline = TypologyInlineFactory.get_instance(typology_type, self.model, self.admin_site)
            if (inline.has_add_permission(request) and 
                    inline.has_change_permission(request, obj) and
                    inline.has_delete_permission(request, obj)):
                inline_instances.append(inline)

        return inline_instances

# Register your models here.
admin.site.register(Question, QuestionAdmin)
