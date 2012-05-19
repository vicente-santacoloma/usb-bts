# Create your views here.
from bugs.forms import BugForm, SelectComponentForm
from bugs.models import Component, Application, Bug
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import FieldError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext

def browse_components(request,application_id):
    application = get_object_or_404(Application,pk=application_id)
    return render_to_response('components/browse.html', {'application': application},
                              context_instance=RequestContext(request))

def browse_bugs(request,application_id, component_id):
    component = get_object_or_404(Component,pk=component_id)
    if not request.GET.__contains__('order_by'):
        orderby = 'title'
    else:
        orderby = request.GET.get('order_by')    
    if orderby not in ('title','visits','priority','description'):
        orderby = 'title'

    bug_list = component.bugs.all().order_by(
                (request.GET.get('order') if request.GET.get('order') == "" or  request.GET.get('order') == "-"  else "" ) + orderby)
        
    paginator = Paginator(bug_list, 25) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        bugs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        bugs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        bugs = paginator.page(paginator.num_pages)
    return render_to_response('bugs/browse.html', {'component': component,
                                                   'bugs': bugs},
                              context_instance=RequestContext(request))

def detail(request, application_id, component_id, bug_id):
    bug = get_object_or_404(Bug,pk=bug_id)
    # THIS IS TOO SIMPLE, RELOAD THE PAGE WILL INCREASE THE VISITS
    bug.visits += 1
    bug.save()
    return render_to_response('bugs/detail.html', {'bug': bug}, 
                              context_instance=RequestContext(request))

def all_json_models(request, application_id):
    current_application = get_object_or_404(Application,pk=application_id)
    components = current_application.components.all()
    json_models = serializers.serialize("json", components)
    return HttpResponse(json_models, mimetype="application/javascript")

@login_required
def report_bug(request,component_id):    
    c =get_object_or_404(Component,pk=component_id)
    if request.method == 'POST':
        bug = Bug(reporter=request.user,component=c)
        form = BugForm(request.POST, instance=bug)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('BTS_home'))       
    else:
        form = BugForm(instance=Bug(component=c))
    return render_to_response('bugs/report.html', 
                                {'form': form },
                                context_instance=RequestContext(request))
    
@login_required
def select_component(request):
    if request.method == 'POST':
        form = SelectComponentForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/bugs/report/' + request.POST['component'] + '/')
    else:        
        form = SelectComponentForm()
    return render_to_response('components/select.html',
                              {'form': form },
                                context_instance=RequestContext(request))