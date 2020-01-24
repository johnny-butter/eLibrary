import braintree
from django.conf import settings
from .base import baseStrategy


class braintreeStrategy(baseStrategy):

    if settings.DEBUG:
        # self.braintree_env = braintree.Environment.Production
        braintree_env = braintree.Environment.Sandbox
    else:
        braintree_env = braintree.Environment.Sandbox

    def __init__(self, **kwargs):
        self.amount = kwargs['amount']
        self.nonce = kwargs['nonce']
        self._result = None
        self._error = []

    @classmethod
    def gateway(cls):
        return braintree.BraintreeGateway(
            braintree.Configuration(
                cls.braintree_env,
                merchant_id=settings.BRAINTREE_MERCHANT_ID,
                public_key=settings.BRAINTREE_PUBLIC_KEY,
                private_key=settings.BRAINTREE_PRIVATE_KEY
            )
        )

    def transaction(self):
        self._result = self.gateway().transaction.sale({
            "amount": str(self.amount),
            "payment_method_nonce": self.nonce,
            "options": {
                "submit_for_settlement": True
            }
        })

    @property
    def success(self):
        if self.result:
            if self.result.is_success:
                return True
            else:
                for error in self.result.errors.deep_errors:
                    self._error.append({
                        'cade': error.code,
                        'message': error.message
                    })

                return False
        else:
            raise ValueError('Execute "transaction" first')
