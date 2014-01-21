# -*- coding: utf-8 -*-
"""
Settings overrided for test time
"""
from app.settings import *
import os 
here = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)

USE_I18N = True
LANGUAGES = (('fr', 'French'),
             ('en', 'English'))


LANGUAGE_CODE = 'en'

TRANSLATION_STRINGS_FILE = here('i18n_strings.py')

def except_south(iterable):
    result = []
    for el in iterable:
        if el != 'south':
            result.append(el)
    return result

INSTALLED_APPS = tuple(except_south(INSTALLED_APPS)) + (
    'app.translations.tests',
)
