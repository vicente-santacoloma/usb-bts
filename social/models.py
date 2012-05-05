from django.db import models

# Create your models here.

class Message(models.Model):
    content = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey('users.user', related_name='messages_sent')
    receiver = models.ForeignKey('users.user', related_name='messages_received')

    def __unicode__(self):
        return "From " + self.sender.get_username() + " to " + self.receiver.get_username() + " on " + self.date_sent + ":\n" + self.content
