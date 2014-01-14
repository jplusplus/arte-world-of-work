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
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin import TabularInline, StackedInline
from django.contrib.contenttypes import generic

from app.core.models import Question, Typology, SelectionTypology


class TypologyAdminForm(forms.ModelForm):
    model = Typology

class InlineTypologyAdmin(admin.TabularInline):
    form = TypologyAdminForm
    model = Typology

class QuestionAdmin(admin.ModelAdmin):
    fields = ('label', 'hint_text', 'typology_type')
    inlines = [
        InlineTypologyAdmin,
    ]

# Register your models here.
admin.site.register(Question, QuestionAdmin)