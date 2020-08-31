from django.db import models


class PublishCompany(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'publish_company'
