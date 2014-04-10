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
# Last Modified time: 2014-04-10 12:18:47
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

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from uuid import uuid4 as uuid 


class WWUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        user = WWUser(username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username, password)
        user.is_staff = user.is_superuser = True
        user.save()
        return user

# Custom User model with UUID as identifier 
class WWUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('User name', max_length=36, unique=True)
    USERNAME_FIELD = 'username'
    objects = WWUserManager()
    is_staff = models.BooleanField(default=False)

    def get_username(self):
        return self.username

    def get_fullname(self):
        return self.get_username()

    def get_short_name(self):
        return self.get_fullname()


    def save(self, *args, **kwargs):
        if not self.username:
            self.username = uuid()
        super(WWUser, self).save(*args, **kwargs)

    def __unicode__(self):
        return "User {id}".format(id=self.username)



