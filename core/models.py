from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, UserManager, AbstractUser
from django.db import models

# Create your models here.
from model_utils.models import TimeStampedModel


class AppUser(AbstractUser):
    twitter_handle = models.CharField(max_length=255)
    user_access_token = models.CharField(max_length=1024, null=True, blank=True)
    user_access_secret = models.CharField(max_length=1024, null=True, blank=True)
    extra_data = models.TextField(null=True, blank=True)
    send_mail = models.BooleanField(default=True)
    unsubscribe = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __unicode__(self):
        if self.first_name and self.last_name:
            return "%s %s" % (self.first_name, self.last_name)
        else:
            return self.username

    class Meta:
        verbose_name_plural = "App Users"


class TweetMasterData(models.Model):
    analytics_request = models.ForeignKey('AnalyticsRequest', related_name='tweets')
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
        unique_together = ("tweet_id", "analytics_request")
        verbose_name_plural = "Tweet Master Data"


class HashTagAnalysisResult(TimeStampedModel):
    analytics_request = models.ForeignKey('AnalyticsRequest', related_name='analytics_results')
    hash_tag = models.CharField(max_length=160)
    positive = models.IntegerField(default=0)
    negative = models.IntegerField(default=0)
    neutral = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s => Positive: %s; Negative: %s; Neutral: %s" % (
            self.hash_tag, self.positive, self.negative, self.neutral)

    class Meta:
        verbose_name_plural = "Has Tag Analysis Results"


class AnalyticsRequest(TimeStampedModel):
    user = models.ForeignKey(AppUser, related_name='hah_tag_analysis_requests')
    status = models.CharField(max_length=25, choices=settings.ANALYTICS_REQUEST_CHOICES)

    def __unicode__(self):
        return "%s %s %s" % (self.user, self.status, self.created)

    class Meta:
        verbose_name_plural = "Analytics Requests"