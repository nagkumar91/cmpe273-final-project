from django.contrib import admin

# Register your models here.
from .models import TweetMasterData, AppUser, AnalyticsRequest, HashTagAnalysisResult, PositiveTweet, NeutralTweet, \
    NegativeTweet

admin.site.register(TweetMasterData)
admin.site.register(AppUser)
admin.site.register(AnalyticsRequest)
admin.site.register(HashTagAnalysisResult)
admin.site.register(PositiveTweet)
admin.site.register(NegativeTweet)
admin.site.register(NeutralTweet)