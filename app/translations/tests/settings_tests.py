# -*- coding: utf-8 -*-
"""
Settings overrided for test time
"""
from django.conf import settings
from app.translations.tests.settings import *

from app import utils

import os 
here = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)
SECRET_KEY = settings.get('SECRET_KEY', 'SHEEEEE')

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

INSTALLED_APPS = tuple(utils.without(INSTALLED_APPS, 'south')) + (
    'app.translations.tests',
)
