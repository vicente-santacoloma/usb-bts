
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from social.models import Message
from django.views.generic.detail import DetailView

urlpatterns = patterns('',
    # regexp, view, options
    url(r'^send_message/$','social.views.send_message'),
    url(r'^message_list/$', login_required(ListView.as_view(model=Message,
                                                            template_name='message_list.html'))),
    url(r'^read_message/(?P<pk>\d+)/$',
        login_required(DetailView.as_view(model=Message, template_name='read_message.html'))),
)