import factory
from api import models
from api.factory import bookTypeFactory, authorFactory
from api.factory.publish_company import publishCompanyFactory


class bookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Book

    name = 'test_book'
    type = factory.SubFactory(bookTypeFactory)
    author = factory.SubFactory(authorFactory)
    publish_company = factory.SubFactory(publishCompanyFactory)
    price_origin = 100
    price_discount = 50
