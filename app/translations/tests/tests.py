# -*- coding: utf-8 -*-
from django.test import TestCase
from django.conf import settings
from django.core.management import call_command

from .models import TestModel

class TranslationsLocalesTestCase(TestCase):
    fixtures = ['/app/translations/tests/fixtures/initial_data.json',]
    def setUp(self):
        pass

    def test_extraction(self): 
        pass 

    def test_translated_field_values(self):
        self.obj = TestModel.objects.get(pk=1)
        val = self.obj.title
        settings.LANGUAGE_CODE = 'fr'
        self.assertEqual(val, 'mon titre')

        settings.LANGUAGE_CODE = 'en'
        self.assertEqual(val, 'my title')


class SyncFromDB(TestCase):

    def test_created_strings(self):
        call_command('sync_db_translations')
        exists = False
        try:
            with open('translations_strings.py'):
                exists = True
        except IOError:
            pass

        self.assertTrue(exists)

