# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'UserProfile.country'
        db.alter_column(u'core_userprofile', 'country', self.gf('django_countries.fields.CountryField')(max_length=2, null=True))

        # Changing field 'UserProfile.age'
        db.alter_column(u'core_userprofile', 'age', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

    def backwards(self, orm):

        # Changing field 'UserProfile.country'
        db.alter_column(u'core_userprofile', 'country', self.gf('django_countries.fields.CountryField')(default='FR', max_length=2))

        # Changing field 'UserProfile.age'
        db.alter_column(u'core_userprofile', 'age', self.gf('django.db.models.fields.PositiveIntegerField')(default=243))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.baseanswer': {
            'Meta': {'object_name': 'BaseAnswer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.BaseQuestion']", 'unique': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'core.basechoicefield': {
            'Meta': {'object_name': 'BaseChoiceField'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.BaseQuestion']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        u'core.basequestion': {
            'Meta': {'object_name': 'BaseQuestion'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'hint_text': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '220'})
        },
        u'core.countryanswer': {
            'Meta': {'object_name': 'CountryAnswer', '_ormbases': [u'core.BaseAnswer']},
            u'baseanswer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseAnswer']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django_countries.fields.CountryField', [], {'max_length': '2'})
        },
        u'core.countryquestion': {
            'Meta': {'object_name': 'CountryQuestion', '_ormbases': [u'core.BaseQuestion']},
            u'basequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseQuestion']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'core.dateanswer': {
            'Meta': {'object_name': 'DateAnswer', '_ormbases': [u'core.BaseAnswer']},
            u'baseanswer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseAnswer']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'core.datequestion': {
            'Meta': {'object_name': 'DateQuestion', '_ormbases': [u'core.BaseQuestion']},
            u'basequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseQuestion']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'core.mediachoicefield': {
            'Meta': {'object_name': 'MediaChoiceField', '_ormbases': [u'core.BaseChoiceField']},
            u'basechoicefield_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseChoiceField']", 'unique': 'True', 'primary_key': 'True'}),
            'picture': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'})
        },
        u'core.mediaradioquestion': {
            'Meta': {'object_name': 'MediaRadioQuestion'},
            u'basequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseQuestion']", 'unique': 'True', 'primary_key': 'True'}),
            'media_type': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        u'core.mediaselectionquestion': {
            'Meta': {'object_name': 'MediaSelectionQuestion'},
            u'basequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseQuestion']", 'unique': 'True', 'primary_key': 'True'}),
            'media_type': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        u'core.numberanswer': {
            'Meta': {'object_name': 'NumberAnswer', '_ormbases': [u'core.BaseAnswer']},
            u'baseanswer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseAnswer']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        u'core.numberquestion': {
            'Meta': {'object_name': 'NumberQuestion', '_ormbases': [u'core.BaseQuestion']},
            u'basequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseQuestion']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'core.questionpicture': {
            'Meta': {'object_name': 'QuestionPicture'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'question': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseQuestion']", 'unique': 'True'})
        },
        u'core.radioanswer': {
            'Meta': {'object_name': 'RadioAnswer', '_ormbases': [u'core.BaseAnswer']},
            u'baseanswer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseAnswer']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.BaseChoiceField']"})
        },
        u'core.selectionanswer': {
            'Meta': {'object_name': 'SelectionAnswer', '_ormbases': [u'core.BaseAnswer']},
            u'baseanswer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseAnswer']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.BaseChoiceField']", 'symmetrical': 'False'})
        },
        u'core.textchoicefield': {
            'Meta': {'object_name': 'TextChoiceField', '_ormbases': [u'core.BaseChoiceField']},
            u'basechoicefield_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseChoiceField']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'core.textradioquestion': {
            'Meta': {'object_name': 'TextRadioQuestion'},
            u'basequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseQuestion']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'core.textselectionquestion': {
            'Meta': {'object_name': 'TextSelectionQuestion'},
            u'basequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseQuestion']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'core.typednumberquestion': {
            'Meta': {'object_name': 'TypedNumberQuestion', '_ormbases': [u'core.BaseQuestion']},
            u'basequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseQuestion']", 'unique': 'True', 'primary_key': 'True'}),
            'max_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': '100'}),
            'min_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        u'core.userageanswer': {
            'Meta': {'object_name': 'UserAgeAnswer', '_ormbases': [u'core.UserProfileAnswer']},
            u'userprofileanswer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.UserProfileAnswer']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'core.useragequestion': {
            'Meta': {'object_name': 'UserAgeQuestion', '_ormbases': [u'core.UserProfileQuestion']},
            u'userprofilequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.UserProfileQuestion']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'core.usercountryanswer': {
            'Meta': {'object_name': 'UserCountryAnswer', '_ormbases': [u'core.UserProfileAnswer']},
            u'userprofileanswer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.UserProfileAnswer']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django_countries.fields.CountryField', [], {'max_length': '2'})
        },
        u'core.usercountryquestion': {
            'Meta': {'object_name': 'UserCountryQuestion', '_ormbases': [u'core.UserProfileQuestion']},
            u'userprofilequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.UserProfileQuestion']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'core.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'age': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'core.userprofileanswer': {
            'Meta': {'object_name': 'UserProfileAnswer', '_ormbases': [u'core.BaseAnswer']},
            u'baseanswer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseAnswer']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'core.userprofilequestion': {
            'Meta': {'object_name': 'UserProfileQuestion', '_ormbases': [u'core.BaseQuestion']},
            u'basequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseQuestion']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['core']