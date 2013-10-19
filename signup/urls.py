from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="signup/index.html"), name='home'),
    url(r'^signup$', 'signup.views.signup', name='signup'),
    url(r'^success$', 'signup.views.signup_success', name='signup_success'),
    url(
        r'^count/(?P<sequence>[\d]+)/$',
        'signup.views.count',
        name='signup_count'
    ),
)
