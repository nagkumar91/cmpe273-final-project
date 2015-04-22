from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext


def homepage(request):
    print request
    return render_to_response("home.html",
                              context_instance=RequestContext(request))


def login_error(request):
    print request
    return HttpResponse("login error")
