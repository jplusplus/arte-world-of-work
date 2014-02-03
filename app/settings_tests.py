#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : Arte - WoW
# -----------------------------------------------------------------------------
# Author : 
# -----------------------------------------------------------------------------
# License : proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 14-Jan-2014
# Last mod : 14-Jan-2014
# -----------------------------------------------------------------------------
from settings import *

INSTALLED_APPS = (
    # ------------------------ django dependencies -------------------------- # 
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    # ------------------------ external dependencies ------------------------ #
    'compressor',
    'django_countries',
    'rest_framework',
    'sorl.thumbnail',
    # ------------------------ internal dependencies ------------------------ # 
    'app.core',
    'app.translations',
)
