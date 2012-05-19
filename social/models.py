from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Message(models.Model):
    content = models.TextField()
    date_sent = models.DateTimeField('date sent',auto_now_add=True)
    sender = models.ForeignKey(User, related_name='messages_sent')
    receiver = models.ForeignKey(User, related_name='messages_received')

    def __unicode__(self):
        return self.content
