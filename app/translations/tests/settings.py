# -*- coding: utf-8 -*-
"""
Settings overrided for test time
"""
from django.conf import settings

INSTALLED_APPS = tuple(settings.INSTALLED_APPS) + (
    'app.translations.tests',
)
USE_I18N = True
LANGUAGES = (('de', 'Deutsch'),
             ('en', 'English'))

LANGUAGE_CODE = 'en'