# -*- coding: utf-8 -*-
from django.test import TestCase
from django.conf import settings

from .models import TestModel

class ExtractLocalesTestCase(TestCase):
    fixtures = ['/app/translations/tests/fixtures/initial_data.json',]
    def setUp(self):
        pass


    def test_translated_field_values(self):
        self.obj = TestModel.objects.get(pk=1)
        val = self.obj.title
        settings.LANGUAGE_CODE = 'fr'
        self.assertEqual(val, 'mon titre')

        settings.LANGUAGE_CODE = 'en'
        self.assertEqual(val, 'my title')