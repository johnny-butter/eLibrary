import string
import random
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.CharField(unique=True, null=True, max_length=254)

    @classmethod
    def random_username(cls):
        letters = string.ascii_letters

        return ''.join([random.choice(letters) for i in range(8)])

    @classmethod
    def random_password(cls):
        letters = string.ascii_letters

        return ''.join([random.choice(letters) for i in range(8)])

    def is_in_group(self, name):
        return self.groups.filter(name=name).exists()
