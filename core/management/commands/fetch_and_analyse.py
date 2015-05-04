import random
import string
from django.core.management import BaseCommand
from django.conf import settings
import datetime
import time
from django.db import IntegrityError
from requests_oauthlib import OAuth1
import requests
from core.models import TweetMasterData as TMD, AppUser
from social_auth.models import UserSocialAuth

__author__ = 'nagkumar'
URL = "https://api.twitter.com/1.1/statuses/home_timeline.json?exclude_replies=true&count=200&"


def transform_time_string(input_str):
    return datetime.datetime.fromtimestamp(time.mktime(time.strptime(input_str, "%a %b %d %H:%M:%S +0000 %Y")))


def unique_hastags(u):
    all_unique_hashtags = []
    for tmd_obj in u.fetched_tweets.all():
        hash_tags = tmd_obj.hash_tags.split(",")
        if not hash_tags[0] == "":
            for ht in hash_tags:
                try:
                    if all_unique_hashtags.index(ht) == -1:
                        pass
                except ValueError:
                    all_unique_hashtags.append(ht)
    return all_unique_hashtags


def get_hashtags(hash_tags_arr):
    returned_tags = ""
    for tag in hash_tags_arr:
        if not returned_tags.__contains__(tag['text']):
            if len(returned_tags) == 0:
                returned_tags = "#%s" % tag['text']
            else:
                returned_tags = "%s,#%s" % (returned_tags, tag['text'])
    return returned_tags


def fetch_200_tweets(auth, u, max_id=None):
    if max_id:
        url = "%smax_id=%s" % (URL, max_id)
    else:
        url = URL
    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        for tweet in response.json():
            hashtags = get_hashtags(tweet['entities']['hashtags'])
            t = TMD(
                owner_id=u,
                created_at=transform_time_string(tweet['created_at']),
                tweet=tweet['text'],
                screen_name=tweet['user']['name'],
                user_name=tweet['user']['screen_name'],
                verified=(True if tweet['user']['verified'] == 'true' else False),
                tweet_id=tweet['id'],
                hash_tags=hashtags
            )
            try:
                t.save()
            except IntegrityError:
                pass
    return 1


def get_data():
    # change this to if user has to be analysed
    max_id = None
    users = AppUser.objects.filter(send_mail=True, unsubscribe=False)
    for user in users:
        try:
            print user
            usa_obj = UserSocialAuth.objects.get(user=user, provider='twitter')
            access_token = usa_obj.tokens.get("oauth_token")
            secret_token = usa_obj.tokens.get("oauth_token_secret")
            auth = OAuth1(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET, access_token,
                          secret_token)
            max_id = fetch_200_tweets(auth, user, max_id)
            unique_hash_tags = unique_hastags(user)
            print unique_hash_tags
        except Exception as e:
            print e
            print "Exception! User not found in keys table"


class Command(BaseCommand):
    help = "Dumps dummy data to the log"

    def handle(self, *args, **options):
        get_data()
