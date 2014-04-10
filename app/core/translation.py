#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# License: GNU General Public License
# -----------------------------------------------------------------------------
# Creation time:      2014-03-21 15:05:09
# Last Modified time: 2014-04-10 12:52:02
# -----------------------------------------------------------------------------
# This file is part of World of Work
# 
#   World of Work is a study about european youth's perception of work
#   Copyright (C) 2014 Journalism++
#   
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#   
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <http://www.gnu.org/licenses/>.

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
    fields = ('title', 'intro_description',)

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
