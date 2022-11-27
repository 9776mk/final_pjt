from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    # username = models.CharField(max_length=16, unique=True)
    followings = models.ManyToManyField("self", symmetrical=False, related_name="followers")