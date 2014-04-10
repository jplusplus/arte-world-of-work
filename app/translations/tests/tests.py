#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# License: GNU General Public License
# -----------------------------------------------------------------------------
# Creation time:      2014-03-21 15:04:05
# Last Modified time: 2014-04-10 12:52:48
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
from django.core.management import call_command
from django.test import TestCase
from django.utils.translation import activate
from django.utils.translation import ugettext, gettext
from app.translations.translator import translator
from app.translations.tests.models import TestModel, InheritedTestModel

import os

class TranslationsLocalesTestCase(TestCase):
    fixtures = ['/app/translations/tests/fixtures/initial_data.json',]

    def test_translated_field_values(self):
        activate('fr')
        obj = TestModel.objects.get(pk=1)
        self.assertEqual(obj.title, 'mon titre')
        activate('en')
        self.assertEqual(obj.title, 'my title')

    def test_translated_field_with_html(self):
        obj = TestModel.objects.get(pk=5)
        activate('en')
        self.assertEqual(obj.title, u'my awesome title <strong>with html</strong>')
        activate('fr')
        self.assertEqual(obj.title, u'mon superbe titre <strong>avec du html</strong>')

    def test_inherited_translated_field_values(self):
        activate('fr')
        obj = InheritedTestModel.objects.get(pk=3)
        self.assertEqual(obj.other, 'une autre traduction')
        self.assertEqual(obj.title, 'mon superbe titre')

        activate('en')
        self.assertEqual(obj.other, 'an other translation')
        self.assertEqual(obj.title, 'my awesome title')

class SyncFromDB(TestCase):

    def test_created_strings(self):
        call_command('sync_db_translations', verbosity=1)
        # we import created python file
        strings_path = settings.TRANSLATION_STRINGS_FILE
        execfile(strings_path)
        _locals = locals()
        self.assertEqual(len(_locals['STRINGS']), 6)

        if os.access(strings_path, os.F_OK):
            os.remove(strings_path)
        if os.access(strings_path + 'c', os.F_OK):
            os.remove(strings_path + 'c')

    def test_translation_options(self):
        opts = translator.get_options_for_model(InheritedTestModel)
        self.assertEqual(len(opts.fields), 2)
        self.assertIsNotNone(opts.fields['title'])
        self.assertIsNotNone(opts.fields['other'])
    
