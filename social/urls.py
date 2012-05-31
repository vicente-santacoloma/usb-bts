
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.core.context_processors import request
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from social.models import Message

urlpatterns = patterns('',
    # regexp, view, options
    url(r'^(?P<user_id>\d+)/$','social.views.send_message'),
    url(r'^$', 'social.views.message_list'),
)