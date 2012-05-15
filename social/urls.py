
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.core.context_processors import request
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from social.models import Message

urlpatterns = patterns('',
    # regexp, view, options
    url(r'^send_message/$','social.views.send_message'),
    url(r'^message_list/$', 'social.views.message_list'),
    url(r'^read_message/(?P<pk>\d+)/$',
        login_required(DetailView.as_view(model=Message, template_name='read_message.html'))),
)