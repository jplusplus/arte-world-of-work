#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project: World of Work
# -----------------------------------------------------------------------------
# Author: Pierre Bellon                               <bellon.pierre@gmail.com>
# -----------------------------------------------------------------------------
# License: GNU General Public License
# -----------------------------------------------------------------------------
# Creation time:      2014-02-18 10:46:32
# Last Modified time: 2014-04-10 12:55:09
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


