from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="signup/index.html")),
    url(r'^signup$', 'signup.views.signup', name='signup'),
)
