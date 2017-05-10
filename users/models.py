from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile_uuid = models.TextField(unique=True)
