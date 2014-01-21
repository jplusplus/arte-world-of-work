# -*- coding: utf-8 -*-
"""
Settings overrided for test time
"""
from app.settings import *

def except_south(iterable):
    result = []
    for el in iterable:
        if el != 'south':
            result.append(el)

    return result

INSTALLED_APPS = tuple(except_south(INSTALLED_APPS)) + (
    'app.translations.tests',
)

USE_I18N = True
LANGUAGES = (('fr', 'French'),
             ('en', 'English'))

LANGUAGE_CODE = 'en'

TRANSLATION_STRING_FILE = here('/translations/strings.py')