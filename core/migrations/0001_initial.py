# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AppUser'
        db.create_table(u'core_appuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('twitter_handle', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('user_access_token', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('user_access_secret', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('send_mail', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('unsubscribe', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'core', ['AppUser'])

        # Adding M2M table for field groups on 'AppUser'
        m2m_table_name = db.shorten_name(u'core_appuser_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('appuser', models.ForeignKey(orm[u'core.appuser'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['appuser_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'AppUser'
        m2m_table_name = db.shorten_name(u'core_appuser_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('appuser', models.ForeignKey(orm[u'core.appuser'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['appuser_id', 'permission_id'])

        # Adding model 'TweetMasterData'
        db.create_table(u'core_tweetmasterdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fetched_tweets', to=orm['core.AppUser'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('tweet', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('screen_name', self.gf('django.db.models.fields.CharField')(max_length=124)),
            ('user_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tweet_id', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('hash_tags', self.gf('django.db.models.fields.CharField')(max_length=1024)),
        ))
        db.send_create_signal(u'core', ['TweetMasterData'])

        # Adding unique constraint on 'TweetMasterData', fields ['tweet_id', 'owner_id']
        db.create_unique(u'core_tweetmasterdata', ['tweet_id', 'owner_id_id'])

        # Adding model 'HashTagAnalysisResult'
        db.create_table(u'core_hashtaganalysisresult', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='hash_tag_analysis_results', to=orm['core.AppUser'])),
            ('hash_tag', self.gf('django.db.models.fields.CharField')(max_length=160)),
            ('positive', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('negative', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('neutral', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'core', ['HashTagAnalysisResult'])


    def backwards(self, orm):
        # Removing unique constraint on 'TweetMasterData', fields ['tweet_id', 'owner_id']
        db.delete_unique(u'core_tweetmasterdata', ['tweet_id', 'owner_id_id'])

        # Deleting model 'AppUser'
        db.delete_table(u'core_appuser')

        # Removing M2M table for field groups on 'AppUser'
        db.delete_table(db.shorten_name(u'core_appuser_groups'))

        # Removing M2M table for field user_permissions on 'AppUser'
        db.delete_table(db.shorten_name(u'core_appuser_user_permissions'))

        # Deleting model 'TweetMasterData'
        db.delete_table(u'core_tweetmasterdata')

        # Deleting model 'HashTagAnalysisResult'
        db.delete_table(u'core_hashtaganalysisresult')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.appuser': {
            'Meta': {'object_name': 'AppUser'},
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
            'send_mail': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'twitter_handle': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'unsubscribe': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_access_secret': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'user_access_token': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'core.hashtaganalysisresult': {
            'Meta': {'object_name': 'HashTagAnalysisResult'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'hash_tag': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'negative': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'neutral': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'positive': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hash_tag_analysis_results'", 'to': u"orm['core.AppUser']"})
        },
        u'core.tweetmasterdata': {
            'Meta': {'unique_together': "(('tweet_id', 'owner_id'),)", 'object_name': 'TweetMasterData'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'hash_tags': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fetched_tweets'", 'to': u"orm['core.AppUser']"}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '124'}),
            'tweet': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tweet_id': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['core']