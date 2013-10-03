from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', 'gallery.views.sequence_redirect', name='gallery_sequence_redirect'),

    url(r'^(?P<sequence>\d)/$', 'gallery.views.gallery', name='gallery_gallery'),

    url(
        r'^(?P<sequence>\d)/save_bio/$',
        'gallery.views.save_bio',
        name='gallery_save_bio'
    ),

    url(
        r'^confirm_updates/(?P<confirmation_code>.*)/$',
        'gallery.views.confirm_updates',
        name='gallery_confirm_update'
    ),

    url(
        r'^request_link/$',
        'gallery.views.request_link',
        name='gallery_request_link'
    ),

    url(r'^clear_session/$', 'gallery.views.clear_session'),
)
