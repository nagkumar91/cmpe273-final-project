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
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('twitter_handle', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('user_access_token', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('user_access_secret', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['AppUser'])

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


    def backwards(self, orm):
        # Removing unique constraint on 'TweetMasterData', fields ['tweet_id', 'owner_id']
        db.delete_unique(u'core_tweetmasterdata', ['tweet_id', 'owner_id_id'])

        # Deleting model 'AppUser'
        db.delete_table(u'core_appuser')

        # Deleting model 'TweetMasterData'
        db.delete_table(u'core_tweetmasterdata')


    models = {
        u'core.appuser': {
            'Meta': {'object_name': 'AppUser'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'email_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'twitter_handle': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user_access_secret': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'user_access_token': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'})
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