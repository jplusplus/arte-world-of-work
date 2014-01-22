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
# Last mod :  2014-01-22 14:39:20
# -----------------------------------------------------------------------------
from django.conf import settings
from django.core.management.base import BaseCommand
from django.template import Context, Template
from optparse import make_option

from app.translations.translator import translator

OPT_STRINGS_ONLY='strings_only'

def extract_strings_from_db():
    strings = []
    models = translator.get_registered_models()
    for (model, opts) in models:
        # loop over model instances
        for instance in model.objects.all():
            for field_name in opts.fields:
                original_string = getattr(instance, 'ref_%s' % field_name, None)
                if original_string is not None:
                    strings.append(original_string)
    return strings

def write_strings(strings):
    template = Template(u'''
_ = lambda s: s
STRINGS = ({% for str in strings %}_("{{ str }}"),{% endfor %})''')
    context = Context({'strings': strings})
    output = template.render(context)
    f = open(settings.TRANSLATION_STRINGS_FILE, 'w+')
    f.write(output)

def sync_strings():
    strings = extract_strings_from_db()
    write_strings(strings)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--strings-only', default=False, dest=OPT_STRINGS_ONLY,
            help='Will update only settings.TRANSLATION_STRINGS_FILE file',
            action='store_true'),
    )
    help = "Synchronize translations strings with database records"

    def handle(self, *args, **opts):
        sync_strings()
