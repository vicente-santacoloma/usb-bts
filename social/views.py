# Create your views here.
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from social.forms import MessageForm
from django.contrib.auth.decorators import login_required

@login_required
def send_message(request):
    if request.method == 'GET':
         return render_to_response('send_message.html', 
                                   {'message': MessageForm()},
                                   context_instance=RequestContext(request))
    elif request.method == 'POST':
         f = MessageForm(request.POST)
         m = f.save(commit=False)
         m.sender = request.user
         m.save()
         return HttpResponseRedirect(reverse('BTS_home'))

def read_message(request):
    pass