from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=16, unique=True)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=128)
    USERS_CHOICES = (
        ('A', 'Administrator'),
        ('G', 'Gate Keeper'),
        ('U', 'User'),
    )
    role = models.CharField(max_length=1, choices=USERS_CHOICES)

    def __unicode__(self):
        return "Username: " + self.username + "\nEmail: " + self.email + "\nRole: " + self.get_role_display()
