import factory
from api import models


class BookTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.BookType

    name = 'test'
