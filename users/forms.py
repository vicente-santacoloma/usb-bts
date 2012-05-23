from django import forms
from django.contrib.auth.models import User
from django.forms.models import ModelForm

class BasicUserChangeForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email',)
        
class SelectUserForm(forms.Form):
    users = User.objects.all()
    choice = [(0,"----------")]
    for u in users:
        choice += [(u.id, u.username)]
    user = forms.ChoiceField(label="Select User",choices=choice)
        
      
