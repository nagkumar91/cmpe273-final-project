from django.contrib import admin

# Register your models here.
from .models import TweetMasterData, AppUser

admin.site.register(TweetMasterData)
admin.site.register(AppUser)