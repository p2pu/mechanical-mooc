from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^confirm/(?P<key>[\w]+)/$', 'unsubscribe.views.confirm',
        name='unsubscribe_confirm'
    ),

    url(r'^$', 'unsubscribe.views.unsubscribe', name='unsubscribe_unsubscribe'),
)
