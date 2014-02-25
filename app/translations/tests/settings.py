# -*- coding: utf-8 -*-
"""
Settings overrided for test time
"""
from app.settings import *
from app import utils

def except_south(iterable):
    return utils.without(iterable, 'south')
 
import os 
here = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)

USE_I18N = True
LANGUAGES = (('fr', 'French'),
             ('en', 'English'))

LANGUAGE_CODE = 'en'

TRANSLATION_STRINGS_FILE = here('i18n_strings.py')

