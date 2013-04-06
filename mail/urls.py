from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^compose/$', 'mail.views.compose', name='mail_compose'),
    url(r'^edit/(?P<id>[\d]+)/$', 'mail.views.edit', name='mail_edit'),
    url(r'^delete/(?P<id>[\d]+)/$', 'mail.views.delete', name='mail_delete'),
    url(r'^send_preview/', 'mail.views.send_preview', name='mail_send_preview'),
    url(r'^schedule/$', 'mail.views.schedule', name='mail_schedule'),
    url(r'^schedule_email/(?P<id>[\d]+)/$', 'mail.views.schedule_email', name='mail_schedule_email'),
)
