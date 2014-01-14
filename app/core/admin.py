from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin import TabularInline, StackedInline
from django.contrib.contenttypes import generic

from app.core.models import Question, Typology

class QuestionAdmin(admin.ModelAdmin):
    fields = ('label', 'hint_text', 'typology_type')

# Register your models here.
admin.site.register(Question, QuestionAdmin)