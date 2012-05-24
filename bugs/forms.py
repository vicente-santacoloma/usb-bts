'''
Created on May 13, 2012

@author: tamerdark
'''
from bugs.models import Bug, Application, Component
from django import forms
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.core.exceptions import ValidationError
from django.db import models
from django.forms.models import ModelForm
from django.forms.util import ErrorList


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
    
def update_status(self, status, resolver=None, original=None, resolution=None):
    pass

class UpdateBugStatusForm(forms.Form):
    status_choices = []
    resolver_choices = [(0, "------------")]
    resolution_choices = Bug.RESOLUTION_CHOICES
    resolution_choices = ((0, "------------"),) + resolution_choices
    original_choices = [(0, "------------")]
    for user in User.objects.all():
        resolver_choices.append( (user.id,user.username) )
    for bug in Bug.objects.all():
        original_choices.append( (bug.id, bug.title) )
    status = forms.ChoiceField(choices=status_choices)
    
    resolver = forms.ChoiceField(choices=resolver_choices,required=False,error_messages = {'invalid_choice': 'Please select an user'})
    resolution = forms.ChoiceField(choices=resolution_choices,required=False, error_messages = {'invalid_choice': 'Please select a solution'})
    original = forms.ChoiceField(choices=original_choices,required=False,error_messages = {'invalid_choice': 'Please select the original bug'})
    
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, 
        initial=None, error_class=ErrorList, label_suffix=':', 
        empty_permitted=False,bug=None):
        forms.Form.__init__(self, data=data, files=files, auto_id=auto_id, prefix=prefix, initial=initial, error_class=error_class, label_suffix=label_suffix, empty_permitted=empty_permitted)
        if not bug is None:
            self.status_choices = bug.get_status_choices()
            self.fields['status'].choices = self.status_choices
    def is_valid(self):
        r = self.fields['resolver'].choices.pop(0)
        s = self.fields['resolution'].choices.pop(0)
        o = self.fields['original'].choices.pop(0)
        ret = forms.Form.is_valid(self)
        self.fields['resolver'].choices.insert(0,r)
        self.fields['original'].choices.insert(0,o)
        self.fields['resolution'].choices.insert(0,s)
        return ret
