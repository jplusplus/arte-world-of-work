#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# License: GNU General Public License
# -----------------------------------------------------------------------------
# Creation time:      2014-03-24 12:40:40
# Last Modified time: 2014-04-10 12:51:37
# -----------------------------------------------------------------------------
# This file is part of World of Work
# 
#   World of Work is a study about european youth's perception of work
#   Copyright (C) 2014 Journalism++
#   
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#   
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Most parts of this translation module come from [django-modeltranslations](1) 
# project distibuted under the following copyright:
# 
# Copyright (c) 2012, 2011, 2010, 2009, Peter Eschler, Dirk Eschler
# All rights reserved.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# 1: https://github.com/deschler/django-modeltranslation

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
