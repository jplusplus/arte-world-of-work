# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'WWUser.uuid'
        db.delete_column(u'authentication_wwuser', 'uuid')

        # Adding field 'WWUser.username'
        db.add_column(u'authentication_wwuser', 'username',
                      self.gf('django.db.models.fields.CharField')(default=0, unique=True, max_length=36),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'WWUser.uuid'
        db.add_column(u'authentication_wwuser', 'uuid',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=36, unique=True),
                      keep_default=False)

        # Deleting field 'WWUser.username'
        db.delete_column(u'authentication_wwuser', 'username')


    models = {
        u'authentication.wwuser': {
            'Meta': {'object_name': 'WWUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36'})
        }
    }

    complete_apps = ['authentication']