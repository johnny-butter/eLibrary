import random
import string
from .base import BaseStrategy


class ManualStrategy(BaseStrategy):

    def __init__(self, **kwargs):
        super(ManualStrategy, self).__init__(**kwargs)
        self.amount = kwargs['amount']

    def transaction(self):
        self._result = True

    @property
    def generate_transaction_id(self):
        string_length = 12
        letters_and_digits = string.ascii_lowercase + string.digits

        return ''.join([random.choice(letters_and_digits) for i in range(string_length)])

    def create_shop_history(self):
        self.pay_order.create_shop_history(
            self.generate_transaction_id,
            self.amount,
            "TWD",
            "manual"
        )

    @property
    def success(self):
        if self.result:
            return True
        else:
            raise ValueError('Execute "transaction" first')
