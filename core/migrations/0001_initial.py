# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.contrib.auth.models
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('twitter_handle', models.CharField(max_length=255)),
                ('user_access_token', models.CharField(max_length=1024, null=True, blank=True)),
                ('user_access_secret', models.CharField(max_length=1024, null=True, blank=True)),
                ('extra_data', models.TextField(null=True, blank=True)),
                ('send_mail', models.BooleanField(default=True)),
                ('unsubscribe', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'App Users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AnalyticsRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('status', models.CharField(max_length=25, choices=[(b'Received Request', b'Received Request'), (b'Processing Request', b'Processing Request'), (b'Sending Email', b'Sending Email'), (b'Email Sent', b'Email Sent')])),
                ('user', models.ForeignKey(related_name='hah_tag_analysis_requests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Analytics Requests',
            },
        ),
        migrations.CreateModel(
            name='HashTagAnalysisResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('hash_tag', models.CharField(max_length=160)),
                ('positive', models.IntegerField(default=0)),
                ('negative', models.IntegerField(default=0)),
                ('neutral', models.IntegerField(default=0)),
                ('analytics_request', models.ForeignKey(related_name='analytics_results', to='core.AnalyticsRequest')),
            ],
            options={
                'verbose_name_plural': 'Has Tag Analysis Results',
            },
        ),
        migrations.CreateModel(
            name='TweetMasterData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField()),
                ('tweet', models.CharField(max_length=255)),
                ('screen_name', models.CharField(max_length=124)),
                ('user_name', models.CharField(max_length=255)),
                ('verified', models.BooleanField(default=False)),
                ('tweet_id', models.CharField(max_length=1024)),
                ('hash_tags', models.CharField(max_length=1024)),
                ('owner_id', models.ForeignKey(related_name='fetched_tweets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Tweet Master Data',
            },
        ),
        migrations.AlterUniqueTogether(
            name='tweetmasterdata',
            unique_together=set([('tweet_id', 'owner_id')]),
        ),
    ]
