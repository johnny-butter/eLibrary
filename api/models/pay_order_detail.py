from django.db import models
from django.utils import timezone


class PayOrderDetail(models.Model):
    pay_order = models.ForeignKey('PayOrder', models.DO_NOTHING)
    book = models.ForeignKey('Book', models.DO_NOTHING)
    quantity = models.IntegerField()
    price = models.DecimalField(
        max_digits=10, decimal_places=3)
    create_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'pay_order_detail'

        indexes = [
            models.Index(fields=['pay_order']),
        ]
