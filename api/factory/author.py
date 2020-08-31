import factory
from api import models


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Author

    name = 'test_author'
