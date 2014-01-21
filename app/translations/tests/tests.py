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
        settings.LANGUAGE_CODE = 'fr'
        self.obj = TestModel.objects.get(pk=1)
        # import pdb; pdb.set_trace()
        val = self.obj.title
        self.assertEqual(val, 'mon titre')

        settings.LANGUAGE_CODE = 'en'
        self.assertEqual(val, 'my title')


class SyncFromDB(TestCase):

    def test_created_strings(self):
        call_command('sync_db_translations')
        from .strings import STRINGS
        self.assertEqual(len(STRINGS), 2)
            

