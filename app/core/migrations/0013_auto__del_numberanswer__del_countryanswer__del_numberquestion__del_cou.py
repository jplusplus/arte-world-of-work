# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):


        # Adding field 'TypedNumberQuestion.validate_button_label'
        db.add_column(u'core_typednumberquestion', 'validate_button_label',
                      self.gf('django.db.models.fields.CharField')(default=u"Done", max_length=120),
                      keep_default=False)

        # Deleting field 'TypedNumberAnswer.numberanswer_ptr'
        db.delete_column(u'core_typednumberanswer', u'numberanswer_ptr_id')

        # Adding field 'TypedNumberAnswer.baseanswer_ptr'
        db.add_column(u'core_typednumberanswer', u'baseanswer_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=1, to=orm['core.BaseAnswer'], unique=True, primary_key=True),
                      keep_default=False)

        # Adding field 'TypedNumberAnswer.value'
        db.add_column(u'core_typednumberanswer', 'value',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


        # Deleting model 'NumberAnswer'
        db.delete_table(u'core_numberanswer')

        # Deleting model 'CountryAnswer'
        db.delete_table(u'core_countryanswer')

        # Deleting model 'NumberQuestion'
        db.delete_table(u'core_numberquestion')

        # Deleting model 'CountryQuestion'
        db.delete_table(u'core_countryquestion')


    def backwards(self, orm):
        # Adding model 'NumberAnswer'
        db.create_table(u'core_numberanswer', (
            (u'baseanswer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseAnswer'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'core', ['NumberAnswer'])

        # Adding model 'CountryAnswer'
        db.create_table(u'core_countryanswer', (
            (u'baseanswer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseAnswer'], unique=True, primary_key=True)),
            ('value', self.gf('django_countries.fields.CountryField')(max_length=2)),
        ))
        db.send_create_signal(u'core', ['CountryAnswer'])

        # Adding model 'NumberQuestion'
        db.create_table(u'core_numberquestion', (
            (u'basequestion_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseQuestion'], unique=True, primary_key=True)),
            ('validate_button_label', self.gf('django.db.models.fields.CharField')(default=u"Done", max_length=120)),
        ))
        db.send_create_signal(u'core', ['NumberQuestion'])

        # Adding model 'CountryQuestion'
        db.create_table(u'core_countryquestion', (
            (u'basequestion_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseQuestion'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'core', ['CountryQuestion'])

        # Deleting field 'TypedNumberQuestion.validate_button_label'
        db.delete_column(u'core_typednumberquestion', 'validate_button_label')

        # Adding field 'TypedNumberAnswer.numberanswer_ptr'
        db.add_column(u'core_typednumberanswer', u'numberanswer_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=1, to=orm['core.NumberAnswer'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'TypedNumberAnswer.baseanswer_ptr'
        db.delete_column(u'core_typednumberanswer', u'baseanswer_ptr_id')

        # Deleting field 'TypedNumberAnswer.value'
        db.delete_column(u'core_typednumberanswer', 'value')


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
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.BaseQuestion']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'core.basechoicefield': {
            'Meta': {'object_name': 'BaseChoiceField'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.BaseQuestion']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        u'core.basefeedback': {
            'Meta': {'object_name': 'BaseFeedback'},
            'html_sentence': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'core.basequestion': {
            'Meta': {'object_name': 'BaseQuestion'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'hint_text': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '220'}),
            'skip_button_label': ('django.db.models.fields.CharField', [], {'default': "u'Skip this question'", 'max_length': '120'})
        },
        u'core.booleanquestion': {
            'Meta': {'object_name': 'BooleanQuestion'},
            u'basequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseQuestion']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'core.numberanswer': {
            'Meta': {'object_name': 'NumberAnswer', '_ormbases': [u'core.BaseAnswer']},
            u'baseanswer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseAnswer']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        u'core.mediachoicefield': {
            'Meta': {'object_name': 'MediaChoiceField', '_ormbases': [u'core.BaseChoiceField']},
            u'basechoicefield_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseChoiceField']", 'unique': 'True', 'primary_key': 'True'}),
            'picture': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'core.mediaradioquestion': {
            'Meta': {'object_name': 'MediaRadioQuestion'},
            u'basequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseQuestion']", 'unique': 'True', 'primary_key': 'True'}),
            'media_type': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        u'core.mediaselectionquestion': {
            'Meta': {'object_name': 'MediaSelectionQuestion'},
            u'basequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseQuestion']", 'unique': 'True', 'primary_key': 'True'}),
            'media_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'validate_button_label': ('django.db.models.fields.CharField', [], {'default': 'u"I\'m done"', 'max_length': '120'})
        },
        u'core.questionmediaattachement': {
            'Meta': {'object_name': 'QuestionMediaAttachement'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
        u'core.staticfeedback': {
            'Meta': {'object_name': 'StaticFeedback', '_ormbases': [u'core.BaseFeedback']},
            u'basefeedback_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseFeedback']", 'unique': 'True', 'primary_key': 'True'}),
            'picture': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'source_title': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
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
            u'basequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseQuestion']", 'unique': 'True', 'primary_key': 'True'}),
            'validate_button_label': ('django.db.models.fields.CharField', [], {'default': 'u"I\'m done"', 'max_length': '120'})
        },
        u'core.thematic': {
            'Meta': {'object_name': 'Thematic'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        u'core.thematicelement': {
            'Meta': {'ordering': "['position']", 'object_name': 'ThematicElement'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thematic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Thematic']", 'null': 'True', 'blank': 'True'})
        },
        u'core.typednumberanswer': {
            'Meta': {'object_name': 'TypedNumberAnswer', '_ormbases': [u'core.BaseAnswer']},
            u'numberanswer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.NumberAnswer']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        u'core.typednumberquestion': {
            'Meta': {'object_name': 'TypedNumberQuestion', '_ormbases': [u'core.BaseQuestion']},
            u'basequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseQuestion']", 'unique': 'True', 'primary_key': 'True'}),
            'max_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': '100'}),
            'min_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'validate_button_label': ('django.db.models.fields.CharField', [], {'default': 'u"I\'m done"', 'max_length': '120'})
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
        u'core.userchoicefield': {
            'Meta': {'object_name': 'UserChoiceField', '_ormbases': [u'core.BaseChoiceField']},
            u'basechoicefield_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseChoiceField']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'})
        },
        u'core.usercountryanswer': {
            'Meta': {'object_name': 'UserCountryAnswer', '_ormbases': [u'core.UserProfileAnswer']},
            u'userprofileanswer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.UserProfileAnswer']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django_countries.fields.CountryField', [], {'max_length': '2'})
        },
        u'core.usercountryquestion': {
            'Meta': {'object_name': 'UserCountryQuestion', '_ormbases': [u'core.UserProfileQuestion']},
            'profile_attribute': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            u'userprofilequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.UserProfileQuestion']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'core.usergenderanswer': {
            'Meta': {'object_name': 'UserGenderAnswer', '_ormbases': [u'core.UserProfileAnswer']},
            u'userprofileanswer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.UserProfileAnswer']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'core.usergenderquestion': {
            'Meta': {'object_name': 'UserGenderQuestion', '_ormbases': [u'core.UserProfileQuestion']},
            u'userprofilequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.UserProfileQuestion']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'core.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'age': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'living_country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'null': 'True'}),
            'native_country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'null': 'True'}),
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