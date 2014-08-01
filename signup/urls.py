from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="signup/index.html"), name='home'),
    url(r'^iframe$', TemplateView.as_view(template_name="signup/iframe.html"), name='home_iframe'),
    url(r'^signup$', 'signup.views.signup', name='signup'),
    url(r'^api/signup/$', 'signup.views.signup_ajax', name='signup_ajax'),
    url(r'^signup/(?P<iframe>true)$', 'signup.views.signup', name='signup_iframe'),
    url(r'^success$', 'signup.views.signup_success', name='signup_success'),
    url(r'^success_iframe$', TemplateView.as_view(template_name='signup/success_iframe.html'), name='signup_success_iframe'),
    url(r'^count/(?P<sequence>[\d]+)/$', 'signup.views.count', name='signup_count'),
    url(r'^export/(?P<sequence>[\d]+)/$', 'signup.views.export', name='signup_export'),
)
