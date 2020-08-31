import factory
from api import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    username = 'test_user'
    password = 'test_user'
    email = 'test@test.com'


class AdminUserFactory(UserFactory):
    username = 'test_admin_user'
    password = 'test_admin_user'
    is_staff = True
