from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'twitter_analytics',
        'USER': 'cmpe273',
        'PASSWORD': 'cmpe273',
        'HOST': '',
        'PORT': '',
    }
}
BROKER_URL = 'amqp://guest:Cmp3273@localhost:5672//'
QUQUEING_REQUESTS = False
# DEBUG = True #temporary
ALLOWED_HOSTS = ['*']
