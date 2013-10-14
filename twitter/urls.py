from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(
        r'^get_twitter_data/$',
        'twitter.views.get_data',
        name='twitter_get_data'
    ),

    url(
        r'^oauth_callback/$',
        'twitter.views.oauth_callback',
        name='twitter_oauth_callback'
    ),
)
