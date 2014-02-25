from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(
        r'^get_profile/$',
        'gplus.views.get_profile',
        name='gplus_get_profile'
    ),
)
