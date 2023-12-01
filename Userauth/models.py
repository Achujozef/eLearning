from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='media/profile_pics/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True,default="")