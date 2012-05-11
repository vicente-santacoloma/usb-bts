from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import Context, loader, RequestContext
from django.contrib.auth.models import User

def home(request):
    return render_to_response('home.html', {} , context_instance=RequestContext(request))
