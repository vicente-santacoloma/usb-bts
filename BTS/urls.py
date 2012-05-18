from BTS import settings
from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BTS.views.home', name='home'),
    # url(r'^BTS/', include('BTS.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'BTS.views.home', name='BTS_home'),
    url(r'^users/', include('users.urls')),
    url(r'^social/', include('social.urls')),
    url(r'^bugs/', include('bugs.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
