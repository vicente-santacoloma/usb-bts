'''
Created on May 10, 2012

@author: tamerdark
'''
from django.forms.models import ModelForm
from social.models import Message

class MessageForm(ModelForm):
    
    class Meta:
        model = Message
        fields = ('content',)