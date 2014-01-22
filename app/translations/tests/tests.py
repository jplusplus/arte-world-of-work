# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.management import call_command
from django.utils.translation import activate

from .models import TestModel

class TranslationsLocalesTestCase(TestCase):
    fixtures = ['/app/translations/tests/fixtures/initial_data.json',]
    def setUp(self):
        pass

    def test_extraction(self): 
        pass 

    def test_translated_field_values(self):
        activate('fr')
        self.obj = TestModel.objects.get(pk=1)
        val = self.obj.title
        self.assertEqual(val, 'mon titre')

        activate('en')
        self.assertEqual(val, 'my title')


class SyncFromDB(TestCase):

    def test_created_strings(self):

        call_command('sync_db_translations')
        # we import created python file
        from .i18n_strings import STRINGS 
        self.assertEqual(len(STRINGS), 2)
            

