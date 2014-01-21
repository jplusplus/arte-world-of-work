# -*- coding: utf-8 -*-
"""
Settings overrided for test time
"""
from django.conf import settings
import os 
here = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)

SECRET_KEY = 'oeoeoeoeooooooooooooooooooooooooeeooeodeffefefef'

USE_I18N = True
LANGUAGES = (('fr', 'French'),
             ('en', 'English'))

LANGUAGE_CODE = 'en'

TRANSLATION_STRINGS_FILE = here('strings.py')

def except_south(iterable):
    result = []
    for el in iterable:
        if el != 'south':
            result.append(el)

    return result

MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES