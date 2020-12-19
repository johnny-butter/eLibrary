import factory
from api import models
from api.factory import BookTypeFactory, AuthorFactory, PublishCompanyFactory


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Book

    name = 'test_book'
    type = factory.SubFactory(BookTypeFactory)
    author = factory.SubFactory(AuthorFactory)
    publish_company = factory.SubFactory(PublishCompanyFactory)
    price_origin = 100
    price_discount = 50
