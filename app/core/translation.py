# -*- coding: utf-8 -*-

from app.core import models
from app.translations.translator import translator, TranslationOptions

# question translation
class QuestionTransOpts(TranslationOptions):
    fields = ('label', 'hint_text', 'skip_button_label')

class ChoiceFieldTransOpts(TranslationOptions):
    fields = ('title', )

class TypedNumberQuestionTransOpts(TranslationOptions):
    fields = ('unit', )

class ThematicTransOpts(TranslationOptions):
    fields = ('title', 'intro_description', 'intro_button_label')

class FeedbackTransOpts(TranslationOptions):
    fields = ('html_sentence', )

class StaticFeedbackTransOpts(TranslationOptions):
    fields = ('source_title', )

translator.register(models.BaseQuestion,        QuestionTransOpts)
translator.register(models.TypedNumberQuestion, TypedNumberQuestionTransOpts)
translator.register(models.BaseChoiceField,     ChoiceFieldTransOpts)
translator.register(models.Thematic,            ThematicTransOpts)
translator.register(models.BaseFeedback,        FeedbackTransOpts)
translator.register(models.StaticFeedback,      StaticFeedbackTransOpts)
