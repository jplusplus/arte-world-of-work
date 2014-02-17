# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.management import call_command
from django.utils.translation import activate
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

class UserTestCase(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username='admin', password='admin')
        self.user  = get_user_model().objects.create_user(
            username='user', password='user')

    def test_call_createsuperuser(self):
        call_command('createsuperuser', interactive=False, username='root')
        superuser = get_user_model().objects.get(username='root')
        superuser.set_password('admin')
        superuser.save()
        self.assertIsNotNone(superuser)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_login_admin(self):
        user = authenticate(username='admin', password='admin')
        self.assertIsNotNone(user)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


