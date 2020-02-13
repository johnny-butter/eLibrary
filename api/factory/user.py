import factory
from api import models


class userFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    username = 'test_user'
    password = 'test_user'
    email = 'test@test.com'


class adminUserFactory(userFactory):
    username = 'test_admin_user'
    password = 'test_admin_user'
    is_staff = True
