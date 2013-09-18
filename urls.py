from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'signup.views.home', name='home'),
    # url(r'^mechanicalmooc/', include('mechanicalmooc.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^about/$', TemplateView.as_view(template_name="about.html"), name="about"),
    url(r'^faq/$', TemplateView.as_view(template_name="faq.html"), name="faq"),
    url(r'', include('signup.urls')),
    url(r'^mail/', include('mail.urls')),
    url(r'^unsubscribe/', include('unsubscribe.urls')),
    url(r'^gallery/', include('gallery.urls')),
    url(r'^twitter/', include('twitter.urls')),
    url(r'accounts/login/', 'django.contrib.auth.views.login'),
)

#TODO - not the best way!
from django.conf import settings

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
