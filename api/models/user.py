from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.CharField(unique=True, null=True, max_length=254)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []
