from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from api.services.pay_strategy import BraintreeStrategy


class BraintreeClientToken(ViewSet):

    def get_client_token(self, request):
        client_token = BraintreeStrategy.gateway().client_token.generate()

        resp = {
            'token': client_token
        }

        return Response(resp)
