import factory
from api import models


class publishCompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PublishCompany

    name = 'test_company'
