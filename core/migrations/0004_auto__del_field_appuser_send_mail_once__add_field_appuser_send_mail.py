# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'AppUser.send_mail_once'
        db.delete_column(u'core_appuser', 'send_mail_once')

        # Adding field 'AppUser.send_mail'
        db.add_column(u'core_appuser', 'send_mail',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'AppUser.send_mail_once'
        db.add_column(u'core_appuser', 'send_mail_once',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Deleting field 'AppUser.send_mail'
        db.delete_column(u'core_appuser', 'send_mail')


    models = {
        u'core.appuser': {
            'Meta': {'object_name': 'AppUser'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'email_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'send_mail': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'twitter_handle': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'unsubscribe': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user_access_secret': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'user_access_token': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'})
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