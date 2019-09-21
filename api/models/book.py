from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=30)
    type = models.ForeignKey('bookType', models.PROTECT)
    author = models.ForeignKey('Author', models.PROTECT, blank=True, null=True)
    publish_company = models.ForeignKey(
        'publishCompany', models.PROTECT, blank=True, null=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    price_origin = models.IntegerField()
    price_discount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'book'
