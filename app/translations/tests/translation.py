from .models import TestModel, InheritedTestModel
from app.translations.translator import translator, TranslationOptions

class TestTranslationOpts(TranslationOptions):
    fields = ('title',)

class InheritedTestTranslationOpts(TranslationOptions):
    fields = ('other',)

translator.register(TestModel, TestTranslationOpts)
translator.register(InheritedTestModel, InheritedTestTranslationOpts)