# Create your views here.
from BTS import settings
from bugs.forms import BugForm, SelectComponentForm, SelectBugStatusForm, \
    AssignBugForm
from bugs.models import Component, Application, Bug
from django.contrib import messages
from django.contrib.auth.decorators import login_required, login_required, \
    permission_required
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core import serializers
from django.core.exceptions import FieldError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404, \
    get_list_or_404
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
    f = AssignBugForm(initial={'bug_id': bug.id})
    status_form = SelectBugStatusForm(initial={'status': bug.status,
                                               'bug_id': bug.id })
    return render_to_response('bugs/detail.html', {'bug': bug, 
                                                   'assign_form': f,
                                                   'status_form': status_form}, 
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

@login_required
@permission_required('bugs.list_unconfirmed_bugs')
def list_unconfirmed_bugs(request):
    bugs = get_list_or_404(Bug,status='U')
    return render_to_response('bugs/unconfirmed.html', 
                                {'bugs': bugs },
                                context_instance=RequestContext(request))
    
@login_required
def list_to_resolve_bugs(request):
    bugs = get_list_or_404(Bug,resolver=request.user)
    return render_to_response('bugs/to_resolve.html', 
                                {'bugs': bugs },
                                context_instance=RequestContext(request))

@login_required
def confirm_bug(request):
    bug = get_object_or_404(Bug,pk=request.POST['bug_id'])
    bug.status = "X"
    bug.save()
    f = AssignBugForm()
    return render_to_response('bugs/detail.html', {'bug': bug, 'f': f}, 
                              context_instance=RequestContext(request))

@login_required
def update_status(request):
    if request.method == 'POST':
        bugF = SelectBugStatusForm(request.POST)
        if bugF.is_valid():
            bug = get_object_or_404(Bug,pk=bugF.cleaned_data['bug_id'])
            bug.status = bugF.cleaned_data['status'];
            if bug.status == Bug.STATUS_DUPLICATED:
                bug.original = Bug.objects.get(pk=bugF.cleaned_data['original'])
            else:
                bug.original = None
            if bug.status != Bug.STATUS_ASSIGNED:
                bug.resolver = None
            # HAY QUE GUARDAR EN LOS COMENTARIOS EL CAMBIO DE STATUS
            bug.save()
            c = Comment()
            c.content_type = ContentType.objects.get(app_label="bugs", model="bug")
            c.object_pk = bug.pk
            c.site = Site.objects.get(id=settings.SITE_ID)
            c.comment = '{0} has changed the status to {1}'.format(request.user.username,
                                                                   bug.get_status_display())
            c.save()
            return HttpResponseRedirect('/bugs/browse/{0}/{1}/{2}'.format(
                                        bug.component.application.id,
                                        bug.component.id,
                                        bug.id))
        else:
            messages.error(request, "An error occur while trying to save the new status.")
            return HttpResponseRedirect(reverse('BTS_home'))
    else:
        return Http404()
    
@login_required
def assign(request):
    if request.method == 'POST':
        assignForm = AssignBugForm(request.POST)
        if assignForm.is_valid():
            bug = get_object_or_404(Bug,pk=assignForm.cleaned_data['bug_id'])
            bug.status = Bug.STATUS_ASSIGNED
            bug.resolver = User.objects.get(pk=assignForm.cleaned_data['user'])
            bug.original = None
            bug.save()
            # HAY QUE GUARDAR EN LOS COMENTARIOS EL CAMBIO DE STATUS
            c = Comment()
            c.content_type = ContentType.objects.get(app_label="bugs", model="bug")
            c.object_pk = bug.pk
            c.site = Site.objects.get(id=settings.SITE_ID)
            c.comment = '{0} has assigned this bug to {1}. Its status has change to {2}'.format(
                                            request.user.username,
                                            bug.resolver.username,
                                            bug.get_status_display())
            c.save()
            return HttpResponseRedirect('/bugs/browse/{0}/{1}/{2}'.format(
                                        bug.component.application.id,
                                        bug.component.id,
                                        bug.id))
        else:
            messages.error(request, "An error occur while trying to assign the bug.")
            return HttpResponseRedirect(reverse('BTS_home'))
    else:
        return Http404()
        