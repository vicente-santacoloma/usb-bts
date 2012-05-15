
from bugs.models import Bug, Component, Application
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

urlpatterns = patterns('bugs.views',
    url(r'^create/$', 'create'),
    url(r'^browse/$', ListView.as_view(model=Application,
                                                      template_name='applications/browse.html')),
    url(r'^browse/(?P<application_id>\d+)/$', 'browse_components'),        
    url(r'^browse/(?P<application_id>\d+)/(?P<component_id>\d+)$', 'browse_bugs'),  
)

urlpatterns += patterns('',
    url(r'^components/create/$', CreateView.as_view(
        model=Component, template_name='components/create.html')
    )
)

