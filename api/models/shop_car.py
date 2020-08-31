from django.db import models
from django.utils import timezone


class ShopCar(models.Model):
    user = models.ForeignKey('User', models.CASCADE)
    book = models.ForeignKey('Book', models.CASCADE)
    quantity = models.IntegerField(default=0)
    create_date = models.DateTimeField(default=timezone.now)
    sold = models.BooleanField(default=False)
    sold_date = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = 'shop_car'
        unique_together = (("user", "book"),)
