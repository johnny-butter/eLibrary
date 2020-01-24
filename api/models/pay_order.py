from django.db import models
from django.utils import timezone
from django_fsm import FSMIntegerField, FSMField, transition
from shared.error_code import PayFail
from api.utils.pay_strategy import payStrategy


class payOrderStateEnum:
    PENDING = 0
    PAID = 1
    SHIPPING = 2
    ARRIVED = 3
    RETURNED = 4
    REFUNDED = 5


class payOrder(models.Model):
    user = models.ForeignKey('User', models.CASCADE)
    state = FSMIntegerField(default=payOrderStateEnum.PENDING)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=3)
    pay_type = models.CharField(max_length=30)
    create_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'pay_order'

    @transition(field=state, source=payOrderStateEnum.PENDING, target=payOrderStateEnum.PAID)
    def pay(self, **kwargs):
        kwargs.update({'amount': self.total_price})

        pay_strategy = payStrategy(self.pay_type, **kwargs).strategy
        pay_strategy.transaction()

        if pay_strategy.success:
            return self, pay_strategy.result
        else:
            resp = {
                'detail': pay_strategy.error,
            }
            raise PayFail(detail=resp)
