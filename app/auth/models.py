# -----------------------------------------------------------------------------
# 
#   Custom user model
# 
# -----------------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class UserProfile(models.Model):
    user    = models.ForeignKey(User, unique=True)
    age     = models.PositiveIntegerField()
    country = CountryField()


