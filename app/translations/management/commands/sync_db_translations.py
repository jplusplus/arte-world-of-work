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
import os
import codecs

TRANSLATION_DEFAULT_LANGUAGE = getattr(settings, 'TRANSLATION_DEFAULT_LANGUAGE', 'en')

def extract_strings_from_db(verbosity=1):
    strings = []
    models = translator.get_registered_models()
    if verbosity > 1:
        print "%s model to register" % len(models)
    for (model, opts) in models:
        # loop over model instances
        for instance in model.objects.all():
            for field_name in opts.fields:
                src_string = getattr(instance, '_%s' % field_name, None)
                if src_string is not None and src_string not in strings:
                    src_string = src_string.replace('"', '\"')
                    strings.append(src_string)

    return strings

def write_strings(strings=(), verbosity=1):
    if verbosity > 1:
        print "%s strings to write" % len(strings)
    template = Template((
            'from django.utils.translation import ugettext_noop as _\n'
            'STRINGS = ('
                '{% for str in strings %}'
                    '{% autoescape off %}'
                    '_("{{ str }}"),'
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
