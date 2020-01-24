from .braintree import braintreeStrategy


class payStrategy:
    strategyMappingDict = {
        'braintree': braintreeStrategy,
    }

    def __init__(self, pay_strategy_name, **kwargs):
        self._pay_strategy = self.strategyMappingDict[pay_strategy_name]
        self.initial_data = kwargs

    @property
    def strategy(self):
        return self._pay_strategy(**self.initial_data)
