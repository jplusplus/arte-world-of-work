# -*- coding: utf-8 -*-
"""
Settings overrided for test time
"""
import os 

here = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)

USE_I18N = True

USE_L10N = True

LANGUAGES = (('fr', 'French'),
             ('en', 'English'))

LANGUAGE_CODE = 'en'

TRANSLATION_STRINGS_FILE = here('i18n_strings.py')

here = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)

SECRET_KEY = 'ttess'

USE_I18N = True
LANGUAGES = (('fr', 'French'),
             ('en', 'English'))

LANGUAGE_CODE = 'en'

TRANSLATION_STRINGS_FILE = here('i18n_strings.py')

DATABASES = {
    'default' : {
        'ENGINE':'django.db.backends.sqlite3',
        'NAME': 'dev.db',
    }
}

INSTALLED_APPS = (
    'app.translations',
    'app.translations.tests',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.i18n',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.locale.LocaleMiddleware',
)


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

LOCALE_PATHS = (
    here('locale/'),
)