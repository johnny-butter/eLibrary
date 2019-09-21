from django.db import models
from django.utils import timezone
from django_fsm import FSMIntegerField, FSMField, transition
from error_code import PayFail


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
    create_date = models.DateTimeField(default=timezone.now())

    class Meta:
        db_table = 'pay_order'

    @transition(field=state, source=payOrderStateEnum.PENDING, target=payOrderStateEnum.PAID)
    def pay(self, pay_method='braintree', braintree_gateway=None, braintree_nonce=None):
        if pay_method == 'braintree':
            result = braintree_gateway.transaction.sale({
                "amount": str(self.total_price),
                "payment_method_nonce": braintree_nonce,
                "options": {
                    "submit_for_settlement": True
                }
            })
            if result.is_success:
                return self, result
            else:
                e = []
                for error in result.errors.deep_errors:
                    e.append({
                        'cade': error.code,
                        'message': error.message
                    })
                raise PayFail(detail={'detail': e})
