# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
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
        # Deleting model 'HashTagAnalysisResult'
        db.delete_table(u'core_hashtaganalysisresult')


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