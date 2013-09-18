from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', 'gallery.views.gallery', name='gallery_gallery'),
    url(r'^save_bio/$', 'gallery.views.save_bio', name='gallery_save_bio'),
    url(r'^success', 'gallery.views.avatar_success', name='gallery_avatar_success'),
    url(r'^confirm_updates/(?P<confirmation_code>.*)/$', 'gallery.views.confirm_updates', name='gallery_confirm_update'),
)
