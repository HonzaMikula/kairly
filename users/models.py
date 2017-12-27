from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    title = models.CharField(max_length=300, blank=True)
    icon_link = models.CharField(max_length=300, blank=True, null=True)
