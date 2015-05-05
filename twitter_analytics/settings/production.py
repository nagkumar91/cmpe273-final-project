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

# DEBUG = True #temporary
ALLOWED_HOSTS = ['*']
