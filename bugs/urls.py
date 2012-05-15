
from bugs.forms import BugForm
from bugs.models import Bug
from django.conf.urls import patterns, include, url
from django.views.generic.edit import CreateView

urlpatterns = patterns('',
    url(r'^create/$', 'bugs.views.create'),
)