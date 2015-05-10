from django.conf.urls import patterns, include, url

urlpatterns = patterns('core.views',
                      url(r'^$', 'homepage'),
                      url(r'^logged-in/$', 'logged_in_page'),
                      url(r'^login-error/$', 'login_error'),
                      url(r'^logged-in/$', 'homepage'),
                      url(r'^login-error/$', 'login_error'),
                      url(r'^unsubscribe/$', 'unsubscribe'),
                      url(r'^user_email/$', 'user_email'),
                      url(r'^get_status/$', 'get_status'),
                      url(r'^start_analytics/$', 'start_analytics'),
                      url(r'^older_results/$', 'older_results'),
                      url(r'^older_result_detail/(?P<id>\d+)/$', 'older_result_detail'),
                      url(r'^edit_profile/$', 'edit_profile'),
                      url(r'^log_out/$', 'log_out'),
)
