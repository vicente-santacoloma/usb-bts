'''
Created on May 13, 2012

@author: tamerdark
'''
from bugs.models import Bug
from django.forms.models import ModelForm


class BugForm(ModelForm):
    class Meta:
        model = Bug
        exclude = ('visits','original', 'reporter','resolver','status')