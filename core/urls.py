from django.conf.urls import patterns, include, url

urlpatterns = patterns('core.views',
                      url(r'^$', 'homepage'),
)
