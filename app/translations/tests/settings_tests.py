# -*- coding: utf-8 -*-
"""
Settings overrided for test time
"""
import os
# from app.settings import *

here = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)

SECRET_KEY = 'SHEEEEE'

USE_I18N = True
LANGUAGES = (('fr', 'French'),
             ('en', 'English'))


LANGUAGE_CODE = 'en'

TRANSLATION_STRINGS_FILE = here('i18n_strings.py')

DATABASES = {
    'default' : {
        'ENGINE':'django.db.backends.sqlite3',
        'NAME': 'test.db'
    }
}

# def remove_apps(apps):
#     apps = filter(
#         lambda x: 'app.translations' in x,
#         apps
#     )
#     return apps


# INSTALLED_APPS = remove_apps(INSTALLED_APPS)

