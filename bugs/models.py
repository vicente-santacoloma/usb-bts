from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import default

class Application(models.Model):
  name = models.CharField(max_length=30, unique=True)
  
  def __unicode__(self):
    return self.name

class Bug(models.Model):
  STATUS_CHOICES = (
        ('U', 'Unconfirmed'),
        ('A', 'Assigned'),
        ('R', 'Resolved'),
        ('D', 'Duplicate'),
        ('C', 'Closed')
  )
  PRIORITY_CHOICES = (
                      ('H','High'),
                      ('N','Normal'),
                      ('L','Low'))
  title = models.CharField(max_length=50)  
  status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='U')
  priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='N')
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