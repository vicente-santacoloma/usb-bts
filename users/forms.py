from django import forms
from django.contrib.auth.models import User
from django.forms.models import ModelForm

class BasicUserChangeForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email',)
        

        
      
