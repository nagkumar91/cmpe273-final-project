from django.db import models

# Create your models here.
from model_utils.models import TimeStampedModel


class AppUser(TimeStampedModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    twitter_handle = models.CharField(max_length=255)
    email_id = models.CharField(max_length=255, null=True, blank=True)
    user_access_token = models.CharField(max_length=1024, null=True, blank=True)
    user_access_secret = models.CharField(max_length=1024, null=True, blank=True)
    send_mail = models.BooleanField(default=True)
    unsubscribe = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        verbose_name_plural = "App Users"


class TweetMasterData(models.Model):
    owner_id = models.ForeignKey(AppUser, related_name='fetched_tweets')
    created_at = models.DateTimeField(auto_now_add=False)
    tweet = models.CharField(max_length=255)
    screen_name = models.CharField(max_length=124)
    user_name = models.CharField(max_length=255)
    verified = models.BooleanField(default=False)
    tweet_id = models.CharField(max_length=1024)
    hash_tags = models.CharField(max_length=1024)

    def __unicode__(self):
        return self.tweet

    class Meta:
        unique_together = ("tweet_id", "owner_id")
        verbose_name_plural = "Tweet Master Data"


class HashTagAnalysisResult(TimeStampedModel):
    user = models.ForeignKey(AppUser, related_name='hash_tag_analysis_results')
    hash_tag = models.CharField(max_length=160)
    positive = models.IntegerField(default=0)
    negative = models.IntegerField(default=0)
    neutral = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s => Positive: %s; Negative: %s; Neutral: %s" % (
            self.hash_tag, self.positive, self.negative, self.neutral)

    class Meta:
        verbose_name_plural = "Has Tag Analysis Results"
