from .models import TestModel
from app.translations.translator import translator, TranslationOptions

class TestTranslationOpts(TranslationOptions):
    fields = ('title',)


translator.register(TestModel, TestTranslationOpts)