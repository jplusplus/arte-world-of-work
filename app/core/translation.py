#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.core.models import *
from app.translations.translator import translator, TranslationOptions

# question translation
class QuestionTransOpts(TranslationOptions):
    fields = ('label', 'hint_text', )

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

translator.register(BaseQuestion,        QuestionTransOpts)
translator.register(TypedNumberQuestion, TypedNumberQuestionTransOpts)
translator.register(BaseChoiceField,     ChoiceFieldTransOpts)
translator.register(Thematic,            ThematicTransOpts)
translator.register(BaseFeedback,        FeedbackTransOpts)
translator.register(StaticFeedback,      StaticFeedbackTransOpts)
