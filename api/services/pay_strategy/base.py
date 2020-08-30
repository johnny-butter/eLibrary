class BaseStrategy:

    def __init__(self, **kwargs):
        self.pay_order = kwargs['pay_order']
        self._result = None
        self._error = []

    def transaction(self):
        '''
        Assign transaction result to self._result
        '''

        raise NotImplementedError

    def create_shop_history(self):
        raise NotImplementedError

    @property
    def result(self):
        return self._result

    @property
    def success(self):
        '''
        Check self.result
        if success
          return True
        else
          assign transaction error messages to self._error
          return False
        '''

        raise NotImplementedError

    @property
    def error(self):
        return self._error
