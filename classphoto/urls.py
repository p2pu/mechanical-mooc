from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', 'classphoto.views.sequence_redirect', name='classphoto_sequence_redirect'),

    url(r'^(?P<sequence>\d)/$', 'classphoto.views.classphoto', name='classphoto_classphoto'),

    url(
        r'^(?P<sequence>\d)/save_bio/$',
        'classphoto.views.save_bio',
        name='classphoto_save_bio'
    ),

    url(
        r'^request_link/$',
        'classphoto.views.request_link',
        name='classphoto_request_link'
    ),

    url(r'^clear_session/$', 'classphoto.views.clear_session'),
)
