# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _ 

class TestModel(models.Model):
    title = models.CharField(_('Title'), max_length=255)
