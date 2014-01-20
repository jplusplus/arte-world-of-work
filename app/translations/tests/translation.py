from .models import TestModel
from app.translations.translator import translator, TranslationOptions

class TestTranslationOpt(TranslationOptions):
    fields = ('title', 'desc')

translator.register(TestModel, TestTranslationsOpts)