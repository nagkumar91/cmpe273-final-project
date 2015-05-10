# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NegativeTweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tweet', models.TextField()),
                ('result_set', models.ForeignKey(related_name='negative_tweets', to='core.HashTagAnalysisResult')),
            ],
        ),
        migrations.CreateModel(
            name='NeutralTweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tweet', models.TextField()),
                ('result_set', models.ForeignKey(related_name='neutral_tweets', to='core.HashTagAnalysisResult')),
            ],
        ),
        migrations.CreateModel(
            name='PositiveTweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tweet', models.TextField()),
                ('result_set', models.ForeignKey(related_name='positive_tweets', to='core.HashTagAnalysisResult')),
            ],
        ),
    ]
