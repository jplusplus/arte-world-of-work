#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : Arte - Wow
# -----------------------------------------------------------------------------
# Author : pbellon
# -----------------------------------------------------------------------------
# License :  proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 2014-01-21 10:25:09
# Last mod :  2014-01-23 10:55:40
# -----------------------------------------------------------------------------
from django.conf import settings
from django.utils import translation
from django.core.management.base import BaseCommand
from django.template import Context, Template

from app.translations.translator import translator
from app.utils import clean_string
import os
import codecs
import re

TRANSLATION_DEFAULT_LANGUAGE = getattr(settings, 'TRANSLATION_DEFAULT_LANGUAGE', 'en')
strings = []

def check_string(str):
    is_valid = str is not None and str not in strings
    is_valid = is_valid and str != " "
    return is_valid 

def extract_strings_from_db(verbosity=1):
    models = translator.get_registered_models()
    if verbosity > 1:
        print "%s model to register" % len(models)
    for (model, opts) in models:
        # loop over model instances
        for instance in model.objects.all():
            for field_name in opts.fields:
                src_string = getattr(instance, '_%s' % field_name, None)
                if check_string(src_string) is True:
                    strings.append(src_string)

    return strings



def write_strings(strings=(), verbosity=1):
    if verbosity > 1:
        print "%s strings to write" % len(strings)
    template = Template((
            'from django.utils.translation import ugettext_noop as _\n'
            'STRINGS = (\n'
                '{% for str in strings %}'
                    '{% autoescape off %}'
                    '\t_("""{{ str }}"""),\n'
                    '{% endautoescape %}'
                '{% endfor %}'
            ')'
        ))
    context = Context({'strings': strings})
    output = template.render(context)

    path = settings.TRANSLATION_STRINGS_FILE
    if os.access(path, os.F_OK):
        os.remove(path)

    if os.access(path + 'c', os.F_OK):
        os.remove(path + 'c')
        
    f = codecs.open(path, 'w', 'utf-8')
    f.write(output)

    if verbosity > 2:
        print "Strings file written at %s:\n\n%s" % (settings.TRANSLATION_STRINGS_FILE, output)

def sync_strings(verbosity=1):
    strings = extract_strings_from_db(verbosity)
    write_strings(strings, verbosity)


class Command(BaseCommand):
    option_list = BaseCommand.option_list
    help = "Synchronize translations strings with database records"

    def handle(self, *args, **opts):
        current_language = translation.get_language()
        translation.activate(TRANSLATION_DEFAULT_LANGUAGE)
        verbosity = int(opts.get('verbosity', 1))
        sync_strings(verbosity)
        translation.activate(current_language)
