# Create your views here.
from debian.debtags import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from social.forms import MessageForm
from social.models import Message


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

@login_required
def message_list(request):
    return render_to_response('message_list.html',
                              {'object_list': Message.objects.filter(sender=request.user)})