from django.db import models
from django.utils import timezone


class shopHistory(models.Model):
    pay_order = models.ForeignKey('payOrder', models.DO_NOTHING)
    transaction_id = models.CharField(max_length=30)
    transaction_total_price = models.DecimalField(
        max_digits=10, decimal_places=3)
    transaction_currency = models.CharField(max_length=5)
    transaction_pay_type = models.CharField(max_length=15)
    create_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_history'
