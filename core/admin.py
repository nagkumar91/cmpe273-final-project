from django.contrib import admin

# Register your models here.
from .models import TweetMasterData, AppUser, AnalyticsRequest, HashTagAnalysisResult

admin.site.register(TweetMasterData)
admin.site.register(AppUser)
admin.site.register(AnalyticsRequest)
admin.site.register(HashTagAnalysisResult)