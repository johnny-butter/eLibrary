from django.db import models
from django.utils import timezone
from django_fsm import FSMIntegerField, transition

from api.services.pay_strategy import PayStrategy
from .shop_history import ShopHistory


class PayError(Exception):

    def __init__(self, error_detail=[], *args):
        super(PayError, self).__init__(*args)
        self.error_detail = {'detail': {'message': error_detail}}


class PayOrderStateEnum:
    PENDING = 0
    PAID = 1
    SHIPPING = 2
    ARRIVED = 3
    RETURNED = 4
    REFUNDED = 5
    CANCEL = 6


class PayOrder(models.Model):
    user = models.ForeignKey('User', models.CASCADE)
    state = FSMIntegerField(default=PayOrderStateEnum.PENDING)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=3)
    pay_type = models.CharField(max_length=30)
    create_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'pay_order'

    def create_shop_history(self, transition_id, total_price, currency, pay_type):
        return ShopHistory.objects.create(
            pay_order=self,
            transaction_id=str(transition_id),
            transaction_total_price=total_price,
            transaction_currency=currency,
            transaction_pay_type=pay_type
        )

    @transition(field=state, source=PayOrderStateEnum.PENDING, target=PayOrderStateEnum.PAID)
    def pay(self, **kwargs):
        kwargs.update({'amount': self.total_price})

        pay_strategy = PayStrategy(self, **kwargs).strategy
        pay_strategy.transaction()

        if pay_strategy.success:
            pay_strategy.create_shop_history()
        else:
            raise PayError(error_detail=pay_strategy.error)

    @transition(field=state, source=PayOrderStateEnum.PENDING, target=PayOrderStateEnum.CANCEL)
    def cancel(self, **kwargs):
        pass
