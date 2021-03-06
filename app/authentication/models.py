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



