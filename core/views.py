from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from social.apps.django_app.default.models import UserSocialAuth
from .models import AnalyticsRequest
from .tasks import queue_analytics_req


def homepage(request):
    return render_to_response("home.html", context_instance=RequestContext(request))


def login_error(request):
    print request
    return HttpResponse("login error")

@login_required()
def logged_in_page(request):
    request.user.unsubscribe = False
    request.user.save()
    for a in UserSocialAuth.objects.all():
        if a.user == request.user:
            request.user.user_access_token = a.extra_data.get("access_token").get("oauth_token")
            request.user.user_access_secret = a.extra_data.get("access_token").get("oauth_token_secret")
            request.user.save()
    return render_to_response("logged_in.html", {'user': request.user}, context_instance=RequestContext(request))


@login_required()
def unsubscribe(request):
    request.user.unsubscribe = True
    request.user.save()
    return render_to_response("unsubscribe.html", {'user': request.user}, context_instance=RequestContext(request))


@login_required()
def user_email(request):
    email_id = request.GET.get("email", None)
    if email_id:
        request.user.email = email_id
        request.user.save()
    return HttpResponse('Thank you')


@login_required()
def get_status(request):
    if request.user.email:
        recent_req = request.users.hah_tag_analysis_requests.all().order_by("-created")
        if len(recent_req) > 0:
            recent_req = recent_req[0]
            return HttpResponse(recent_req.status)
        else:
            return HttpResponseBadRequest()
    return HttpResponseNotFound()


@csrf_exempt
@login_required()
def start_analytics(request):
    email_id = request.user.email
    if email_id:
        analytics_request_obj = AnalyticsRequest(user=request.user, status=settings.ANALYTICS_NEW_REQUEST_CHOICE)
        analytics_request_obj.save()
        queue_analytics_req.delay(analytics_request_obj)
        return HttpResponse('Accepted')
    return HttpResponseBadRequest()