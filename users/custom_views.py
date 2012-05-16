'''
Created on May 15, 2012

@author: tamerdark
'''
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView


class UserUpdateView(UpdateView):
    def get_object(self, queryset=None):
        obj = User.objects.get(username=self.request.user)
        return obj