# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^sign_up/$', 'users.views.sign_up'),
    url(r'^log_in/$', 'users.views.log_in'),
    url(r'^log_out/$', 'users.views.log_out'),
)
