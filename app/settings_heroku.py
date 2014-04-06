#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : Arte-WoW
# -----------------------------------------------------------------------------
# Author : toutenrab
# -----------------------------------------------------------------------------
# License :  proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 2014-01-23 11:28:04
# Last mod :  2014-01-23 15:03:39
# -----------------------------------------------------------------------------
from settings import *
import dj_database_url

DATABASES = {
    'default' : dj_database_url.config()
}

ROOT_URLCONF = 'app.urls'

ALLOWED_HOSTS = [
                "arte-wow-staging.herokuapp.com", 
                "arte-wow-production.herokuapp.com", 
                ".herokuapp.com"
            ]

AWS_ACCESS_KEY_ID          = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY      = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME    = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_FILE_OVERWRITE      = os.getenv('AWS_S3_FILE_OVERWRITE') == "True" and True or False

DEBUG                      = bool(os.getenv('DEBUG', 0))

LANGUAGE_CODE              = os.getenv('LANGUAGE_CODE', 'fr')

STATIC_URL                 = os.getenv('STATIC_URL')

STATIC_ROOT                = here('staticfiles')

STATICFILES_DIRS           = (here('static'),)

INSTALLED_APPS            += ('storages',)

DEFAULT_FILE_STORAGE       = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE        = DEFAULT_FILE_STORAGE


COMPRESS_CSS_FILTERS = (
    "app.utils.CustomCssAbsoluteFilter",
    "compressor.filters.cssmin.CSSMinFilter",
    "compressor.filters.template.TemplateFilter",
)

COMPRESS_JS_FILTERS = (
    "compressor.filters.jsmin.JSMinFilter",
    "compressor.filters.template.TemplateFilter",
)

COMPRESS_TEMPLATE_FILTER_CONTEXT = {
    'STATIC_URL': STATIC_URL
}

AUTH_USER_MODEL = 'authentication.WWUser'

COMPRESSOR_ROOT      = STATIC_ROOT
COMPRESSOR_URL       = STATIC_URL
COMPRESS_STORAGE     = STATICFILES_STORAGE
COMPRESS_ENABLED     = True
COMPRESS_OFFLINE     = True
AWS_QUERYSTRING_AUTH = False
TINYMCE_JS_URL       = STATIC_URL + 'arte_ww/vendor/tinymce/tinymce.min.js'
LOCAL_SETTINGS       = False

# Configure cache
os.environ['MEMCACHE_SERVERS']  = os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';')
os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')

CACHES = {
  'default': {
    'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
    'TIMEOUT': 60*60*1, # One hour
    'BINARY': True,
    'OPTIONS': {
        'tcp_nodelay': True,
        'remove_failed': 4
    }
  }
}

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # Cache middlewares
    'django.contrib.messages.middleware.MessageMiddleware',    
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware'
)

# EOF
