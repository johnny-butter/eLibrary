from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Book(models.Model):
    name = models.CharField(max_length=30)
    type = models.ForeignKey('bookType', models.PROTECT)
    author = models.ForeignKey('Author', models.PROTECT, blank=True, null=True)
    publish_company = models.ForeignKey(
        'publishCompany', models.PROTECT, blank=True, null=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    price_origin = models.IntegerField()
    price_discount = models.IntegerField(blank=True, null=True)
    stock = models.IntegerField(default=0)
    update_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'book'


@receiver(pre_save, sender=Book)
def record_update_time(sender, instance, **kwargs):
    instance.update_at = timezone.now()
