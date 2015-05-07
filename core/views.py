from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from social.apps.django_app.default.models import UserSocialAuth

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
