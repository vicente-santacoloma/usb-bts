'''
Created on May 13, 2012

@author: tamerdark
'''
from bugs.models import Bug, Application, Component
from django import forms
from django.contrib.comments.models import Comment
from django.db import models
from django.forms.models import ModelForm


class BugForm(ModelForm):    
    class Meta:
        model = Bug
        exclude = ('component','date_changed','visits','original', 'reporter','resolver','status')
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
    application = forms.ChoiceField(choices=APP_CHOICES)
    comps = Component.objects.all()
    COMP_CHOICES = []
    for comp in comps:
        COMP_CHOICES.append((comp.id, comp.name))
    component = forms.ChoiceField(choices=COMP_CHOICES)
    