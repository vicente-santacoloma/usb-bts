from django.forms.models import ModelForm
from django.contrib.auth.models import User

def BasicUserChangeForm(ModelForm):
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name')
        