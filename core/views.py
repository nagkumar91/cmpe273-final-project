from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render, render_to_response, redirect

# Create your views here.
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from social.apps.django_app.default.models import UserSocialAuth
from core.start_analysis import start
from .models import AnalyticsRequest, HashTagAnalysisResult
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
    logout(request)
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
        if settings.QUQUEING_REQUESTS:
            queue_analytics_req.delay(analytics_request_obj)
        else:
            start(analytics_request_obj)
        return HttpResponse('Accepted')

    return HttpResponseBadRequest()


@login_required()
def older_results(request):
    new_request = request.GET.get("new", None)
    previous_requests = request.user.hah_tag_analysis_requests.all().order_by("-created")
    return render_to_response("previous_analysis.html",
                                {
                                    'previous_requests': previous_requests,
                                    'user': request.user,
                                    'new_request': new_request
                                },
                              )


@login_required()
def older_result_detail(request, id):
    try:
        analysis_req = AnalyticsRequest.objects.get(pk=id)
        return render_to_response("detailed_analysis.html",
            {
                'results': analysis_req.analytics_results.all().order_by("-positive", "-negative")
            }
        )
    except ObjectDoesNotExist:
        return HttpResponseNotFound()


@login_required()
def older_result_detail_with_hash(request, result_id):
    try:
        analysis_result = HashTagAnalysisResult.objects.get(pk=result_id)
        if request.user == analysis_result.analytics_request.user:
            positive_tweets = analysis_result.positive_tweets.all()
            negative_tweets = analysis_result.negative_tweets.all()
            neutral_tweets  = analysis_result.neutral_tweets.all()

            return render_to_response("detailed_analysis_with_tweets.html",
                {
                    'result': analysis_result,
                    'positive_tweets': positive_tweets,
                    'negative_tweets': negative_tweets,
                    'neutral_tweets': neutral_tweets
                })
        return HttpResponseBadRequest()
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

@csrf_exempt
def mail_delivered(request):
    print request
    return HttpResponse('OK')


@csrf_exempt
@login_required()
def edit_profile(request):
    if request.method == 'GET':
        return render_to_response("edit_profile.html", {'user': request.user, 'updated': False},
                                  context_instance=RequestContext(request))
    else:
        new_mail_id = request.POST.get("email")
        receive_email = request.POST.get("checkboxes")
        print request.POST.get("checkboxes")
        try:
            if receive_email[0] is "True":
                request.user.send_mail = True
        except TypeError:
            request.user.send_mail = False
        request.user.email = new_mail_id
        request.user.save()

        return render_to_response("edit_profile.html", {'user': request.user, 'updated': True},
                                  context_instance=RequestContext(request))


@login_required()
def log_out(request):
    logout(request)
    return redirect('/')
