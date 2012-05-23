'''
Created on May 13, 2012

@author: tamerdark
'''
from bugs.models import Bug, Application, Component
from django import forms
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.db import models
from django.forms.models import ModelForm


class BugForm(ModelForm):    
    class Meta:
        model = Bug
        exclude = ('component','date_changed','visits','original', 'reporter','resolver','status','resolution')
        #widgets = {
        #    'component': forms.HiddenInput(),
        # }
        
class CustomCommentForm(ModelForm):
    class Meta:
        model = Comment
        
class SelectComponentForm(forms.Form):
    apps = Application.objects.all()
    APP_CHOICES = [("0","Select an application")]
    for app in apps:
        APP_CHOICES.append((app.id, app.name))
    comps = Component.objects.all()
    COMP_CHOICES = []
    for comp in comps:
        COMP_CHOICES.append((comp.id, comp.name))
    application = forms.ChoiceField(choices=APP_CHOICES)
    component = forms.ChoiceField(choices=COMP_CHOICES)
    
class SelectBugStatusForm(forms.Form):
    c = []
    for v , d in Bug.STATUS_CHOICES:
        if v != Bug.STATUS_UNCONFIRMED:
            c += [(v,d)]
    bug_id = forms.IntegerField(widget=forms.models.HiddenInput)
    status = forms.ChoiceField(choices=c)
    b = []
    for bug in Bug.objects.all():
        b += [(bug.id, bug.title)]
    original = forms.ChoiceField(choices=b, required = False)
    
class AssignBugForm(forms.Form):
    users = User.objects.all()
    choice = [(0,"----------")]
    for u in users:
        choice += [(u.id, u.username)]
    user = forms.ChoiceField(label="Select User",choices=choice)
    bug_id = forms.IntegerField(widget=forms.models.HiddenInput)