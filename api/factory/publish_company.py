import factory
from api import models


class PublishCompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PublishCompany

    name = 'test_company'
