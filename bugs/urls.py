
from bugs.forms import BugForm
from bugs.models import Bug, Component, Application
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

urlpatterns = patterns('bugs.views',
    url(r'^report/$', 'select_component'),
    url(r'^report/(?P<component_id>\d+)/$', 'report_bug'),
    url(r'^browse/$', ListView.as_view(model=Application,
                                        template_name='applications/browse.html')),
    url(r'^browse/(?P<application_id>\d+)/$', 'browse_components'),        
    url(r'^browse/(?P<application_id>\d+)/(?P<component_id>\d+)/$', 'browse_bugs'),
    url(r'^browse/(?P<application_id>\d+)/(?P<component_id>\d+)/(?P<bug_id>\d+)/$', 'detail'), 
    url(r'^json/(?P<application_id>\d+)/$', 'all_json_models'),
    url(r'^unconfirmed/$', 'list_unconfirmed_bugs'),
    url(r'^to_resolve/$','list_to_resolve_bugs'),
    url(r'^confirm/$','confirm_bug'),
    url(r'^update_status/(?P<bug_id>\d+)/$', 'update_status'),
    url(r'^assign/$', 'assign'),
)

urlpatterns += patterns('',
    url(r'^components/create/$', CreateView.as_view(
        model=Component, template_name='components/create.html')
    )
)
