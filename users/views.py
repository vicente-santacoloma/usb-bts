# -*- coding: utf-8 -*-
# Create your views here.

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import Context, loader, RequestContext
from django.contrib.auth.models import User

def sign_up(request):
    try:
      username = request.POST['username']
      email = request.POST['email']
      password = request.POST['password']
      User.objects.create_user(username, email, password)
    except(KeyError):
      return render_to_response('users/sign_up.html', {} , context_instance=RequestContext(request))
    else:
      pass
    return HttpResponseRedirect("Sign up ok")
