# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from app.utils import db_table_exists

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'DateQuestion'
        if db_table_exists(u'core_datequestion'):
            db.delete_table(u'core_datequestion')

        # Deleting model 'QuestionPicture'
        if db_table_exists(u'core_questionpicture'):
            db.delete_table(u'core_questionpicture')

        # Deleting model 'DateAnswer'
        if db_table_exists(u'core_dateanswer'):
            db.delete_table(u'core_dateanswer')

        # Deleting model 'MediaSelectionQuestion'
        if db_table_exists(u'core_mediaselectionquestion'):
            db.delete_table(u'core_mediaselectionquestion')

        # Adding model 'BaseFeedback'
        if not db_table_exists(u'core_basefeedback'):
            db.create_table(u'core_basefeedback', (
                (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('html_sentence', self.gf('django.db.models.fields.CharField')(max_length=120)),
        ))
        db.send_create_signal(u'core', ['BaseFeedback'])

        # Adding model 'StaticFeedback'
        if not db_table_exists(u'core_staticfeedback'):
            db.create_table(u'core_staticfeedback', (
                (u'basefeedback_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseFeedback'], unique=True, primary_key=True)),
            ('source_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('source_title', self.gf('django.db.models.fields.CharField')(max_length=120)),
        ))
        db.send_create_signal(u'core', ['StaticFeedback'])

        # Adding model 'QuestionMediaAttachement'
        if not db_table_exists(u'core_questionmediaattachement'):
            db.create_table(u'core_questionmediaattachement', (
                (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
                ('picture', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100)),
                ('question', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseQuestion'], unique=True)),
            ))
            db.send_create_signal(u'core', ['QuestionMediaAttachement'])

        # Adding field 'TextSelectionQuestion.validate_button_label'
        db.add_column(u'core_textselectionquestion', 'validate_button_label',
                      self.gf('django.db.models.fields.CharField')(default=u"Done", max_length=120),
                      keep_default=False)


        # Changing field 'ThematicElement.position'
        db.alter_column(u'core_thematicelement', 'position', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))
        # Adding field 'NumberQuestion.validate_button_label'
        db.add_column(u'core_numberquestion', 'validate_button_label',
                      self.gf('django.db.models.fields.CharField')(default=u"Done", max_length=120),
                      keep_default=False)

        # Adding field 'BaseQuestion.skip_button_label'
        db.add_column(u'core_basequestion', 'skip_button_label',
                      self.gf('django.db.models.fields.CharField')(default=u'Skip this question', max_length=120),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'DateQuestion'
        if not db_table_exists(u'core_datequestion'):
            db.create_table(u'core_datequestion', (
                (u'basequestion_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseQuestion'], unique=True, primary_key=True)),
            ))
            db.send_create_signal(u'core', ['DateQuestion'])

        # Adding model 'QuestionPicture'
        if not db_table_exists(u'core_questionpicture'):
            db.create_table(u'core_questionpicture', (
                ('picture', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100)),
                ('question', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseQuestion'], unique=True)),
                (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ))
            db.send_create_signal(u'core', ['QuestionPicture'])

        # Adding model 'DateAnswer'
        if not db_table_exists(u'core_dateanswer'):
            db.create_table(u'core_dateanswer', (
                (u'baseanswer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseAnswer'], unique=True, primary_key=True)),
                ('value', self.gf('django.db.models.fields.DateTimeField')()),
            ))
            db.send_create_signal(u'core', ['DateAnswer'])

        # Adding model 'MediaSelectionQuestion'
        if not db_table_exists(u'core_mediaselectionquestion'):
            db.create_table(u'core_mediaselectionquestion', (
                (u'basequestion_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseQuestion'], unique=True, primary_key=True)),
                ('media_type', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ))
            db.send_create_signal(u'core', ['MediaSelectionQuestion'])

        # Deleting model 'BaseFeedback'
        if db_table_exists(u'core_basefeedback'):
            db.delete_table(u'core_basefeedback')

        # Deleting model 'StaticFeedback'
        if db_table_exists(u'core_staticfeedback'):
            db.delete_table(u'core_staticfeedback')

        # Deleting model 'QuestionMediaAttachement'
        if db_table_exists(u'core_questionmediaattachement'):
            db.delete_table(u'core_questionmediaattachement')

        # Deleting field 'TextSelectionQuestion.validate_button_label'
        db.delete_column(u'core_textselectionquestion', 'validate_button_label')


        # Changing field 'ThematicElement.position'
        db.alter_column(u'core_thematicelement', 'position', self.gf('django.db.models.fields.PositiveIntegerField')(default=0))
        # Deleting field 'NumberQuestion.validate_button_label'
        db.delete_column(u'core_numberquestion', 'validate_button_label')

        # Deleting field 'BaseQuestion.skip_button_label'
        db.delete_column(u'core_basequestion', 'skip_button_label')


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
        u'core.countryanswer': {
            'Meta': {'object_name': 'CountryAnswer', '_ormbases': [u'core.BaseAnswer']},
            u'baseanswer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseAnswer']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django_countries.fields.CountryField', [], {'max_length': '2'})
        },
        u'core.countryquestion': {
            'Meta': {'object_name': 'CountryQuestion', '_ormbases': [u'core.BaseQuestion']},
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
        u'core.numberanswer': {
            'Meta': {'object_name': 'NumberAnswer', '_ormbases': [u'core.BaseAnswer']},
            u'baseanswer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseAnswer']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        u'core.numberquestion': {
            'Meta': {'object_name': 'NumberQuestion', '_ormbases': [u'core.BaseQuestion']},
            u'basequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseQuestion']", 'unique': 'True', 'primary_key': 'True'}),
            'validate_button_label': ('django.db.models.fields.CharField', [], {'default': 'u"Done"', 'max_length': '120'})
        },
        u'core.questionmediaattachement': {
            'Meta': {'object_name': 'QuestionMediaAttachement'},
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
        u'core.staticfeedback': {
            'Meta': {'object_name': 'StaticFeedback', '_ormbases': [u'core.BaseFeedback']},
            u'basefeedback_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseFeedback']", 'unique': 'True', 'primary_key': 'True'}),
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
            'validate_button_label': ('django.db.models.fields.CharField', [], {'default': 'u"Done"', 'max_length': '120'})
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
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'thematic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Thematic']", 'null': 'True'})
        },
        u'core.typednumberanswer': {
            'Meta': {'object_name': 'TypedNumberAnswer', '_ormbases': [u'core.NumberAnswer']},
            u'numberanswer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.NumberAnswer']", 'unique': 'True', 'primary_key': 'True'})
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