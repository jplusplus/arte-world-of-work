from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from uuid import uuid4 as uuid 

class WWUserManager(BaseUserManager):
    def create_user(self):
        user = WWUser()
        user.save()
        return user

# Custom User model with UUID as identifier 
class WWUser(AbstractBaseUser):
    uuid = models.CharField(max_length=36, unique=True)
    objects = WWUserManager()
    USERNAME_FIELD = 'uuid'
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid()
        super(WWUser, self).save(*args, **kwargs)

    def __unicode__(self):
        return "User {id}".format(id=self.uuid)
