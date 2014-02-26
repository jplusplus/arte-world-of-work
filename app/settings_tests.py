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

def without(iter, el): return filter(lambda x: x!=el, iter)

INSTALLED_APPS = without(INSTALLED_APPS, 'south') + (
    'app.translations.tests',
)
