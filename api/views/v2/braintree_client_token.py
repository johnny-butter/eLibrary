from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from api.utils.pay_strategy import braintreeStrategy


class braintreeClientToken(ViewSet):

    def getClientToken(self, request):
        client_token = braintreeStrategy.gateway().client_token.generate()

        resp = {
            'token': client_token
        }

        return Response(resp)
