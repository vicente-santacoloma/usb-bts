from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class UserProfile(models.Model):
      
    class Meta:
        permissions = (
            ("gatekeeper", "The user is a gatekeeper"),
        )  
    
    # Required field
    user = models.OneToOneField(User)

# Asegurarse de crear el UserProfile luego de guardar una instancia de usuario
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
