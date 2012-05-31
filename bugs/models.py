# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import default
import datetime

class Application(models.Model):
    name = models.CharField(max_length=30, unique=True)
  
    def __unicode__(self):
        return self.name

class Bug(models.Model):

    STATUS_UNCONFIRMED = 1
    STATUS_CONFIRMED = 2
    STATUS_ASSIGNED = 3
    STATUS_RESOLVED = 5
    STATUS_VERIFIED = 6
    STATUS_REOPENED = 7
    STATUS_CLOSED = 8
    STATUS_CHOICES = (
          (STATUS_UNCONFIRMED, 'Unconfirmed'),
          (STATUS_CONFIRMED, 'Confirmed'),
          (STATUS_ASSIGNED, 'Assigned'),
          (STATUS_RESOLVED, 'Resolved'),
          (STATUS_VERIFIED, 'Verified'),
          (STATUS_CLOSED, 'Closed'),
          (STATUS_REOPENED, 'Reopened')
    )
    PRIORITY_HIGH = 'H'
    PRIORITY_NORMAL = 'N'
    PRIORITY_LOW = 'L'
    PRIORITY_CHOICES = (
                        (PRIORITY_HIGH,'High'),
                        (PRIORITY_NORMAL,'Normal'),
                        (PRIORITY_LOW,'Low'))
    title = models.CharField(max_length=50)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_UNCONFIRMED)
    RESOLUTION_FIXED = 1
    RESOLUTION_DUPLICATED = 2
    RESOLUTION_WONTFIX = 3
    RESOLUTION_WORKSFORME = 4
    RESOLUTION_INVALID = 5
    RESOLUTION_CHOICES = (
                        (RESOLUTION_FIXED,'Fixed'),
                        (RESOLUTION_DUPLICATED,'Duplicated'),
                        (RESOLUTION_WONTFIX,"Won't fix"),
                        (RESOLUTION_WORKSFORME,"Wrong resolution"),
                        (RESOLUTION_INVALID,"Invalid"))
    resolution = models.IntegerField(choices=RESOLUTION_CHOICES, null=True, blank=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default=PRIORITY_NORMAL)
    date_reported = models.DateTimeField('date reported', auto_now_add=True)
    date_changed = models.DateTimeField('date changed', null=True, blank=True)
    description = models.TextField()
    replication = models.TextField(verbose_name= "How to replicate the error?")
    visits = models.IntegerField(default=0)
    original = models.ForeignKey('Bug', related_name='duplicates', null=True, blank=True)
    reporter = models.ForeignKey(User, related_name='bugs_reported')
    resolver = models.ForeignKey(User, related_name='bugs_resolving', null=True, blank=True)
    component = models.ForeignKey('Component', related_name='bugs')
    
    def __unicode__(self):
        return self.title
    
    def is_assignable(self):
        return self.status in (Bug.STATUS_UNCONFIRMED,
                              Bug.STATUS_CONFIRMED,
                              Bug.STATUS_REOPENED,)
        
    def is_confirmable(self):
        return self.status in (Bug.STATUS_UNCONFIRMED,
                              Bug.STATUS_ASSIGNED,)
        
    def is_resolvable(self):
        return self.status in (Bug.STATUS_UNCONFIRMED,
                              Bug.STATUS_CONFIRMED,
                              Bug.STATUS_REOPENED,
                              Bug.STATUS_ASSIGNED,)
        
    def is_verifiable(self):
        return self.status in (Bug.STATUS_RESOLVED,)
    
    def is_closeable(self):
        return self.status in (Bug.STATUS_RESOLVED,
                                   Bug.STATUS_VERIFIED,)
    
    def is_reopenable(self):
        return self.status in (Bug.STATUS_CLOSED,
                                   Bug.STATUS_VERIFIED,)
    
    def has_been_confirmed(self):
        return self.status != self.STATUS_UNCONFIRMED
    
    def update_status(self, status, resolver=None, original=None, resolution=None):
        status = int(status)
        if status == Bug.STATUS_CONFIRMED:
            print "Trying to update to confirmed"
            if self.is_confirmable():
                self.resolver = None
                self.status = status
                print "The bug has been confirmed"
            else:
                return False
        elif status == Bug.STATUS_ASSIGNED:
            if self.is_assignable() and not resolver is None:
                self.resolver = resolver
                self.status = status
            else:
                return False       
        elif status == Bug.STATUS_RESOLVED:
            if self.is_resolvable() and not resolution is None:
                if resolution == Bug.RESOLUTION_DUPLICATED:
                    if original is None or original == self:
                        return False
                    self.original = original
                self.resolution = resolution
                self.status = status
                if not self.resolver: 
                    if resolver is None:
                        return False
                    self.resolver = resolver
            else:
                return False
        elif status == Bug.STATUS_VERIFIED:
            if self.is_verifiable() :
                self.status = status
                return True
        elif status == Bug.STATUS_CLOSED:
            if self.is_closeable() :
                self.status = status
            else:
                return False
        elif status == Bug.STATUS_REOPENED:
            if self.is_reopenable() :
                self.resolver = None
                self.resolution = None
                self.original = None
                self.status = status
            else:
                return False
        self.date_changed = datetime.date.today()
        return True
    
    def get_status_choices(self):
        choices = [(0, 'Select status')]
        if self.is_confirmable():
            choices.append((self.STATUS_CONFIRMED, 'Confirmed'))
        if self.is_assignable():
            choices.append((self.STATUS_ASSIGNED, 'Assigned'))
        if self.is_resolvable():
            choices.append((self.STATUS_RESOLVED, 'Resolved'))
        if self.is_verifiable():
            choices.append((self.STATUS_VERIFIED, 'Verified'))
        if self.is_closeable():
            choices.append((self.STATUS_CLOSED, 'Closed'))
        if self.is_reopenable():
            choices.append((self.STATUS_REOPENED, 'Reopened'))
        return choices


class Component(models.Model):
    name = models.CharField(max_length=30, unique=True)
    application = models.ForeignKey(Application, related_name='components')
  
    def __unicode__(self):
        return self.name
    
class Comment(models.Model):
    content = models.TextField()
    bug = models.ForeignKey(Bug)
    user_notes = models.ForeignKey(User)
  
    def __unicode__(self):
        return self.content
