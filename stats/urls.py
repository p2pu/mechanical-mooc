from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(
        r'^signup_count/(?P<sequence>[\d]+)/$',
        'stats.views.signup_count', 
        name='stats_signup_count'
    ),
)
