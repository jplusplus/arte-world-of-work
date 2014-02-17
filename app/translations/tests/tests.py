# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.management import call_command
from django.utils.translation import activate

from .models import TestModel

class TranslationsLocalesTestCase(TestCase):
    fixtures = ['/app/translations/tests/fixtures/initial_data.json',]
    def setUp(self):
        pass

    def test_translated_field_values(self):
        activate('fr')
        obj = TestModel.objects.get(pk=1)
        self.assertEqual(obj.title, 'mon titre')

        activate('en')
        self.assertEqual(obj.title, 'my title')


class SyncFromDB(TestCase):

    def test_created_strings(self):

        call_command('sync_db_translations', verbosity=1)
        # we import created python file
        from app.i18n_strings import STRINGS
        self.assertEqual(len(STRINGS), 2)
            

