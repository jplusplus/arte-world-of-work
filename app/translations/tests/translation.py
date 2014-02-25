from .models import TestModel, InheritedTestModel
from django.conf import settings
if getattr(settings, 'IS_LOCAL', False):
    from translations.translator import translator, TranslationOptions
else:
    from app.translations.translator import translator, TranslationOptions

class TestTranslationOpts(TranslationOptions):
    fields = ('title',)

class InheritedTestTranslationOpts(TranslationOptions):
    fields = ('other',)

translator.register(TestModel, TestTranslationOpts)
translator.register(InheritedTestModel, InheritedTestTranslationOpts)
