import factory
from api import models


class bookTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.BookType

    name = 'test'
