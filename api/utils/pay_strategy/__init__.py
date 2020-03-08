from .braintree import braintreeStrategy


class payStrategy:
    strategyMappingDict = {
        'braintree': braintreeStrategy,
    }

    def __init__(self, pay_order, **kwargs):
        self._pay_strategy = self.strategyMappingDict[pay_order.pay_type]

        kwargs.update({'pay_order': pay_order})
        self.initial_data = kwargs

    @property
    def strategy(self):
        return self._pay_strategy(**self.initial_data)
