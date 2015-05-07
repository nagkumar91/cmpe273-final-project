from django.conf.urls import patterns, include, url

urlpatterns = patterns('core.views',
                      url(r'^$', 'homepage'),
                      url(r'^logged-in/$', 'logged_in_page'),
                      url(r'^login-error/$', 'login_error'),
                      url(r'^logged-in/$', 'homepage'),
                      url(r'^login-error/$', 'login_error'),
                      url(r'^unsubscribe/$', 'unsubscribe'),
)
