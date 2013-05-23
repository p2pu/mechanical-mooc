from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^unsubscribe/$', 'unsubscribe.views.unsubscribe_webhook', name='unsubscribe_unsubscribe'),
)
