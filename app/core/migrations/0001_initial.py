# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CountryAnswer'
        db.create_table(u'core_countryanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.BaseQuestion'])),
            ('value', self.gf('django_countries.fields.CountryField')(max_length=2)),
        ))
        db.send_create_signal(u'core', ['CountryAnswer'])

        # Adding model 'NumberAnswer'
        db.create_table(u'core_numberanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.BaseQuestion'])),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'core', ['NumberAnswer'])

        # Adding model 'DateAnswer'
        db.create_table(u'core_dateanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.BaseQuestion'])),
            ('value', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'core', ['DateAnswer'])

        # Adding model 'SelectionAnswer'
        db.create_table(u'core_selectionanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.BaseQuestion'])),
        ))
        db.send_create_signal(u'core', ['SelectionAnswer'])

        # Adding M2M table for field value on 'SelectionAnswer'
        m2m_table_name = db.shorten_name(u'core_selectionanswer_value')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('selectionanswer', models.ForeignKey(orm[u'core.selectionanswer'], null=False)),
            ('basechoicefield', models.ForeignKey(orm[u'core.basechoicefield'], null=False))
        ))
        db.create_unique(m2m_table_name, ['selectionanswer_id', 'basechoicefield_id'])

        # Adding model 'RadioAnswer'
        db.create_table(u'core_radioanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.BaseQuestion'])),
            ('value', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.BaseChoiceField'])),
        ))
        db.send_create_signal(u'core', ['RadioAnswer'])

        # Adding model 'BaseQuestion'
        db.create_table(u'core_basequestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=220)),
            ('hint_text', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
        ))
        db.send_create_signal(u'core', ['BaseQuestion'])

        # Adding model 'NumberQuestion'
        db.create_table(u'core_numberquestion', (
            (u'basequestion_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseQuestion'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'core', ['NumberQuestion'])

        # Adding model 'TypedNumberQuestion'
        db.create_table(u'core_typednumberquestion', (
            (u'basequestion_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseQuestion'], unique=True, primary_key=True)),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('min_number', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('max_number', self.gf('django.db.models.fields.PositiveIntegerField')(default=100)),
        ))
        db.send_create_signal(u'core', ['TypedNumberQuestion'])

        # Adding model 'DateQuestion'
        db.create_table(u'core_datequestion', (
            (u'basequestion_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseQuestion'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'core', ['DateQuestion'])

        # Adding model 'CountryQuestion'
        db.create_table(u'core_countryquestion', (
            (u'basequestion_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseQuestion'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'core', ['CountryQuestion'])

        # Adding model 'QuestionPicture'
        db.create_table(u'core_questionpicture', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('picture', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100)),
            ('question', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseQuestion'], unique=True)),
        ))
        db.send_create_signal(u'core', ['QuestionPicture'])

        # Adding model 'TextSelectionQuestion'
        db.create_table(u'core_textselectionquestion', (
            (u'basequestion_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseQuestion'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'core', ['TextSelectionQuestion'])

        # Adding model 'TextRadioQuestion'
        db.create_table(u'core_textradioquestion', (
            (u'basequestion_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseQuestion'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'core', ['TextRadioQuestion'])

        # Adding model 'MediaSelectionQuestion'
        db.create_table(u'core_mediaselectionquestion', (
            (u'basequestion_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseQuestion'], unique=True, primary_key=True)),
            ('media_type', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal(u'core', ['MediaSelectionQuestion'])

        # Adding model 'MediaRadioQuestion'
        db.create_table(u'core_mediaradioquestion', (
            (u'basequestion_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseQuestion'], unique=True, primary_key=True)),
            ('media_type', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal(u'core', ['MediaRadioQuestion'])

        # Adding model 'BaseChoiceField'
        db.create_table(u'core_basechoicefield', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.BaseQuestion'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=120)),
        ))
        db.send_create_signal(u'core', ['BaseChoiceField'])

        # Adding model 'TextChoiceField'
        db.create_table(u'core_textchoicefield', (
            (u'basechoicefield_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseChoiceField'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'core', ['TextChoiceField'])

        # Adding model 'MediaChoiceField'
        db.create_table(u'core_mediachoicefield', (
            (u'basechoicefield_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseChoiceField'], unique=True, primary_key=True)),
            ('picture', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['MediaChoiceField'])


    def backwards(self, orm):
        # Deleting model 'CountryAnswer'
        db.delete_table(u'core_countryanswer')

        # Deleting model 'NumberAnswer'
        db.delete_table(u'core_numberanswer')

        # Deleting model 'DateAnswer'
        db.delete_table(u'core_dateanswer')

        # Deleting model 'SelectionAnswer'
        db.delete_table(u'core_selectionanswer')

        # Removing M2M table for field value on 'SelectionAnswer'
        db.delete_table(db.shorten_name(u'core_selectionanswer_value'))

        # Deleting model 'RadioAnswer'
        db.delete_table(u'core_radioanswer')

        # Deleting model 'BaseQuestion'
        db.delete_table(u'core_basequestion')

        # Deleting model 'NumberQuestion'
        db.delete_table(u'core_numberquestion')

        # Deleting model 'TypedNumberQuestion'
        db.delete_table(u'core_typednumberquestion')

        # Deleting model 'DateQuestion'
        db.delete_table(u'core_datequestion')

        # Deleting model 'CountryQuestion'
        db.delete_table(u'core_countryquestion')

        # Deleting model 'QuestionPicture'
        db.delete_table(u'core_questionpicture')

        # Deleting model 'TextSelectionQuestion'
        db.delete_table(u'core_textselectionquestion')

        # Deleting model 'TextRadioQuestion'
        db.delete_table(u'core_textradioquestion')

        # Deleting model 'MediaSelectionQuestion'
        db.delete_table(u'core_mediaselectionquestion')

        # Deleting model 'MediaRadioQuestion'
        db.delete_table(u'core_mediaradioquestion')

        # Deleting model 'BaseChoiceField'
        db.delete_table(u'core_basechoicefield')

        # Deleting model 'TextChoiceField'
        db.delete_table(u'core_textchoicefield')

        # Deleting model 'MediaChoiceField'
        db.delete_table(u'core_mediachoicefield')


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
            'Meta': {'object_name': 'CountryAnswer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.BaseQuestion']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'value': ('django_countries.fields.CountryField', [], {'max_length': '2'})
        },
        u'core.countryquestion': {
            'Meta': {'object_name': 'CountryQuestion', '_ormbases': [u'core.BaseQuestion']},
            u'basequestion_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseQuestion']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'core.dateanswer': {
            'Meta': {'object_name': 'DateAnswer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.BaseQuestion']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
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
            'Meta': {'object_name': 'NumberAnswer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.BaseQuestion']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
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
            'Meta': {'object_name': 'RadioAnswer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.BaseQuestion']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'value': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.BaseChoiceField']"})
        },
        u'core.selectionanswer': {
            'Meta': {'object_name': 'SelectionAnswer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.BaseQuestion']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
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
        }
    }

    complete_apps = ['core']