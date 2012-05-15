# Create your views here.
from bugs.forms import BugForm
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
 