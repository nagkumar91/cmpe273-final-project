import datetime
import time
from django.conf import settings
from django.db import IntegrityError
import requests
from requests_oauthlib import OAuth1
from .models import TweetMasterData, HashTagAnalysisResult, NeutralTweet, PositiveTweet, NegativeTweet
from twitter_analytics.nltk_interface import TweetsClassifier
from django.template.loader import get_template

URL = "https://api.twitter.com/1.1/statuses/home_timeline.json?exclude_replies=true&count=200&"
classifier_object = TweetsClassifier()


def transform_time_string(input_str):
    return datetime.datetime.fromtimestamp(time.mktime(time.strptime(input_str, "%a %b %d %H:%M:%S +0000 %Y")))


def get_hashtags(hash_tags_arr):
    returned_tags = ""
    for tag in hash_tags_arr:
        if not returned_tags.__contains__(tag['text']):
            if len(returned_tags) == 0:
                returned_tags = "#%s" % tag['text'].lower()
            else:
                returned_tags = "%s,#%s" % (returned_tags, tag['text'].lower())
    return returned_tags


def fetch_tweet(analytics_req_obj):
    auth = OAuth1(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET,
                  analytics_req_obj.user.user_access_token,
                  analytics_req_obj.user.user_access_secret)
    response = requests.get(URL, auth=auth)
    if response.status_code == 200:
        for tweet in response.json():
            hashtags = get_hashtags(tweet['entities']['hashtags'])
            t = TweetMasterData(
                analytics_request=analytics_req_obj,
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


def get_unique_hastags(analytics_req_obj):
    all_unique_hashtags = []
    for tmd_obj in analytics_req_obj.tweets.all():
        hash_tags = tmd_obj.hash_tags.split(",")
        if not hash_tags[0] == "":
            for ht in hash_tags:
                try:
                    if all_unique_hashtags.index(ht) == -1:
                        pass
                except ValueError:
                    all_unique_hashtags.append(ht)
    return all_unique_hashtags


def analyse_tweet(tweet, hastag):
    if hastag.lower() in tweet.lower():
        resp = classifier_object.classify(tweet)
        if resp is "pos":
            return settings.TWEET_IS_POSITIVE
        else:
            return settings.TWEET_IS_NEGATIVE
    return settings.TWEET_IS_NEUTRAL


def send_complex_message(html_content, to_id):
    return requests.post(
        settings.MAILGUN_URL,
        auth=("api", settings.MAILGUN_API_KEY),
        data={"from": "CMPE 273 Twitter analytics <twitter_analytics@nagkumar.com>",
              "to": to_id,
              "subject": "Here is your report",
              "text": "This is what we found!",
              "html": html_content})


def generate_content(analytics_req_obj):
    all_results = analytics_req_obj.analytics_results.all().order_by("-positive", "-negative")
    template = get_template("email_template.html")
    return template.render({'all_results': all_results, 'user': analytics_req_obj.user})


def start(analytics_req_obj):
    analytics_req_obj.status = settings.ANALYTICS_PROCESSING_REQUEST_CHOICE
    analytics_req_obj.save()
    fetch_tweet(analytics_req_obj)

    unique_hash_tags = get_unique_hastags(analytics_req_obj)
    for hashtag in unique_hash_tags:
        postive_count = negative_count = neutral_count = 0
        htar = HashTagAnalysisResult(
            analytics_request=analytics_req_obj,
            hash_tag=hashtag,
            positive=postive_count,
            negative=negative_count,
            neutral=neutral_count,
        )
        htar.save()
        for tweet in analytics_req_obj.tweets.all():
            res = analyse_tweet(tweet.tweet, hashtag)
            if res == settings.TWEET_IS_NEUTRAL:
                neutral_count += 1
                o = NeutralTweet(result_set=htar, tweet=tweet.tweet)
                o.save()
            elif res == settings.TWEET_IS_POSITIVE:
                postive_count += 1
                o = PositiveTweet(result_set=htar, tweet=tweet.tweet)
                o.save()
            else:
                o = NegativeTweet(result_set=htar, tweet=tweet.tweet)
                o.save()
                negative_count += 1
        htar.positive = postive_count
        htar.negative = negative_count
        htar.neutral = neutral_count
        htar.save()


    html_content = generate_content(analytics_req_obj)
    analytics_req_obj.status = settings.ANALYTICS_SENDING_EMAIL_CHOICE
    analytics_req_obj.save()
    status = send_complex_message(html_content, analytics_req_obj.user.email)

    #webhook should change the status here
    analytics_req_obj.status = settings.ANALYTICS_EMAIL_SENT_CHOICE
    analytics_req_obj.save()

