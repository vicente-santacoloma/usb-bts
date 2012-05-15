# Create your views here.
from bugs.forms import BugForm
from bugs.models import Component, Application
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

@login_required
def create(request):
    if request.method == 'POST':
        form = BugForm(request.POST)
        if form.is_valid():
            bug = form.save(commit=False)
            bug.reporter = request.user
            bug.save()
            return HttpResponseRedirect(reverse('BTS_home'))
            
    else: 
        form = BugForm()
    return render_to_response('create.html',
                                  {'form': form},context_instance=RequestContext(request))

def browse_components(request,application_id):
    application = Application.objects.get(pk=application_id)
    return render_to_response('components/browse.html', {'application': application})

def browse_bugs(request,application_id, component_id):
    component = Component.objects.get(pk=component_id)
    return render_to_response('bugs/browse.html', {'component': component})