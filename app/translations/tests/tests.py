# -*- coding: utf-8 -*-
from django.conf import settings 
from django.core.management import call_command
from django.test import TestCase
from django.utils.translation import activate

from translations.translator import translator
from translations.tests.models import TestModel, InheritedTestModel

import os

class TranslationsLocalesTestCase(TestCase):
    fixtures = ['/app/translations/tests/fixtures/initial_data.json',]
    

    def test_translated_field_values(self):
        activate('fr')
        obj = TestModel.objects.get(pk=1)
        self.assertEqual(obj.title, 'mon titre')
        activate('en')
        self.assertEqual(obj.title, 'my title')

    def test_inherited_translated_field_values(self):
        activate('fr')
        obj = InheritedTestModel.objects.get(pk=3)
        self.assertEqual(obj.title, 'mon superbe titre')
        self.assertEqual(obj.other, 'une autre traduction')

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
        self.assertEqual(len(_locals['STRINGS']), 5)

        if os.access(strings_path, os.F_OK):
            os.remove(strings_path)
        if os.access(strings_path + 'c', os.F_OK):
            os.remove(strings_path + 'c')


            

    def test_translation_options(self):
        opts = translator.get_options_for_model(InheritedTestModel)
        self.assertEqual(len(opts.fields), 2)
        self.assertIsNotNone(opts.fields['title'])
        self.assertIsNotNone(opts.fields['other'])
    
