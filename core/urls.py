from django.conf.urls import patterns, include, url

urlpatterns = patterns('core.views',
                      url(r'^$', 'homepage'),
                      url(r'^logged-in/$', 'homepage'),
                      url(r'^login-eoor/$', 'login_error'),
)
