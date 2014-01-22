#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : Arte - Wow
# -----------------------------------------------------------------------------
# Author : pbellon
# -----------------------------------------------------------------------------
# License :  proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 2014-01-21 10:25:09
# Last mod :  2014-01-22 18:19:52
# -----------------------------------------------------------------------------
from django.conf import settings
from django.core.management.base import BaseCommand
from django.template import Context, Template
from optparse import make_option

from app.translations.translator import translator

OPT_STRINGS_ONLY='strings_only'

def extract_strings_from_db(verbosity=1):
    strings = []
    models = translator.get_registered_models()
    if verbosity > 1:
        print "%s model to register" % len(models)
    for (model, opts) in models:
        # loop over model instances
        for instance in model.objects.all():
            for field_name in opts.fields:
                original_string = getattr(instance, '_%s' % field_name, None)
                if original_string is not None:
                    strings.append(original_string)
    return strings

def write_strings(strings=(), verbosity=1):
    if verbosity > 1:
        print "%s strings to write" % len(strings)
    template = Template(u'''
_ = lambda s: s
STRINGS = ({% for str in strings %}_("{{ str }}"),{% endfor %})''')
    context = Context({'strings': strings})
    output = template.render(context)

    f = open(settings.TRANSLATION_STRINGS_FILE, 'w+')
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
        verbosity = opts.get('verbosity', 1)
        sync_strings(verbosity)
