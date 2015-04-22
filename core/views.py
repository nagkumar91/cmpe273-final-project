from django.http import HttpResponse
from django.shortcuts import render, render_to_response

# Create your views here.


def homepage(request):
    return render_to_response("home.html")
