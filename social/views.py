# Create your views here.
from debian.debtags import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from social.forms import MessageForm
from social.models import Message


@login_required
def send_message(request, user_id):
    u = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            m = form.save(commit=False)
            m.sender = request.user
            m.receiver = u
            m.save()
            return HttpResponseRedirect("/social/%s/" % user_id)
    else:
        form = MessageForm()
    messages = Message.objects.filter( Q(sender=request.user, receiver=u) | Q(receiver=request.user, sender=u)).order_by("-date_sent")
    return render_to_response("send_message.html", {'messages_list': messages,
                                                    'form': form}, 
                              context_instance=RequestContext(request))

@login_required
def message_list(request):
    list_1 = Message.objects.filter(sender=request.user)
    list_2 = Message.objects.filter(receiver=request.user)
    list = []
    for l in list_1:
        if not (l.receiver in list):
            list += [l.receiver]
            
    for l in list_2:
        if not (l.sender in list):
            list += [l.sender]
    
    return render_to_response('message_list.html',
                              {'object_list': list,
                               'user' : request.user})
    
