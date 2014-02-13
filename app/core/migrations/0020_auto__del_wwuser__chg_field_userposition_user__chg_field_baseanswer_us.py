# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'WWUser'
        db.delete_table(u'core_wwuser')

        db.create_table(u'authentication_wwuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('uuid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=36)),
        ))
        db.send_create_signal(u'authentication', ['WWUser'])


        # Changing field 'UserPosition.user'
        db.alter_column(u'core_userposition', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['authentication.WWUser'], unique=True))

        # Changing field 'BaseAnswer.user'
        db.alter_column(u'core_baseanswer', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['authentication.WWUser']))

        # Changing field 'UserProfile.user'
        db.alter_column(u'core_userprofile', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['authentication.WWUser'], unique=True))

    def backwards(self, orm):
        # Adding model 'WWUser'
        db.delete_table(u'authentication_wwuser')
        db.create_table(u'core_wwuser', (
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, unique=True)),
        ))
        db.send_create_signal(u'core', ['WWUser'])


        # Changing field 'UserPosition.user'
        db.alter_column(u'core_userposition', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.WWUser'], unique=True))

        # Changing field 'BaseAnswer.user'
        db.alter_column(u'core_baseanswer', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.WWUser']))

        # Changing field 'UserProfile.user'
        db.alter_column(u'core_userprofile', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.WWUser'], unique=True))

    models = {
        u'authentication.wwuser': {
            'Meta': {'object_name': 'WWUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36'})
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
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['authentication.WWUser']"})
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
            'validate_button_label': ('django.db.models.fields.CharField', [], {'default': "u'Done'", 'max_length': '120'})
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
            'validate_button_label': ('django.db.models.fields.CharField', [], {'default': "u'Done'", 'max_length': '120'})
        },
        u'core.thematic': {
            'Meta': {'ordering': "('position',)", 'object_name': 'Thematic'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro_button_label': ('django.db.models.fields.CharField', [], {'default': "u'See the data'", 'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'intro_description': ('django.db.models.fields.TextField', [], {}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
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
            u'baseanswer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseAnswer']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        u'core.typednumberquestion': {
            'Meta': {'object_name': 'TypedNumberQuestion', '_ormbases': [u'core.BaseQuestion']},
            u'basequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseQuestion']", 'unique': 'True', 'primary_key': 'True'}),
            'max_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': '100'}),
            'min_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'validate_button_label': ('django.db.models.fields.CharField', [], {'default': "u'Done'", 'max_length': '120'})
        },
        u'core.userageanswer': {
            'Meta': {'object_name': 'UserAgeAnswer', '_ormbases': [u'core.UserProfileAnswer']},
            u'userprofileanswer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.UserProfileAnswer']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'core.useragequestion': {
            'Meta': {'object_name': 'UserAgeQuestion', '_ormbases': [u'core.UserProfileQuestion']},
            u'userprofilequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.UserProfileQuestion']", 'unique': 'True', 'primary_key': 'True'}),
            'validate_button_label': ('django.db.models.fields.CharField', [], {'default': "u'Done'", 'max_length': '120'})
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
        u'core.userposition': {
            'Meta': {'object_name': 'UserPosition'},
            'element_position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'thematic_position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['authentication.WWUser']", 'unique': 'True'})
        },
        u'core.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'age': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'living_country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'null': 'True'}),
            'native_country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['authentication.WWUser']", 'unique': 'True'})
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