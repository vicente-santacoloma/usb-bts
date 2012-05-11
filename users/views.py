# -*- coding: utf-8 -*-
# Create your views here.

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import Context, loader, RequestContext
from django.core.context_processors import csrf

def sign_up(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'GET':
        return render_to_response('sign_up.html',c)
    elif request.method == 'POST':
        try:
          username = request.POST['username']
          email = request.POST['email']
          password = request.POST['password']
          User.objects.create_user(username, email, password)
        except(KeyError):
          return render_to_response('sign_up.html',c)
        else:
          pass
    return HttpResponseRedirect(reverse('BTS_home'))

def log_in(request):
    c = {}
    c.update(csrf(request))
    if (request.method == 'GET') and not request.user.is_authenticated():
        return render_to_response('log_in.html',c)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
    return HttpResponseRedirect(reverse('BTS_home'))


def log_out(request):
  logout(request)
  return HttpResponseRedirect(reverse('BTS_home'))
