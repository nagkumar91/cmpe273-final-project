from __future__ import absolute_import

from celery import shared_task
from .start_analysis import start


@shared_task
def queue_analytics_req(analytics_req_object):
    print "Task Started"
    return start(analytics_req_object)