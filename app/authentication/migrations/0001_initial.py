# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WWUser'
        db.create_table(u'authentication_wwuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('uuid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=36)),
        ))
        db.send_create_signal(u'authentication', ['WWUser'])


    def backwards(self, orm):
        # Deleting model 'WWUser'
        db.delete_table(u'authentication_wwuser')


    models = {
        u'authentication.wwuser': {
            'Meta': {'object_name': 'WWUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36'})
        }
    }

    complete_apps = ['authentication']