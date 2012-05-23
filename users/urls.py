# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.views import login, logout, password_change, \
    password_reset
from django.core.context_processors import request
from django.template.context import RequestContext
from django.views.generic.edit import CreateView, UpdateView
from users.forms import BasicUserChangeForm

urlpatterns = patterns('',
    #url(r'^sign_up/$', CreateView.as_view(form_class=UserCreationForm,
    #                                     template_name='sign_up.html',
    #                                     success_url='/')),
    url(r'^sign_up/$', 'users.views.sign_up'),
    url(r'^login/$', login, {'template_name':'login.html'}),
    url(r'^logout/$', logout, {'next_page':'/'}),
    url(r'^password_change/$', password_change, {'template_name': 'password_change.html',
                                                 'post_change_redirect': '/'}),
    url(r'^password_reset/$', password_reset, {'template_name': 'password_reset.html',
                                                 'email_template_name': 'password_reset_email.html',
                                                 'subject_template_name': 'password_reset_subject.txt',
                                                 'post_reset_redirect': '/'}),
    url(r'change/$', 'users.views.update'),
#   url(r'assign/$', assign_user)
)
