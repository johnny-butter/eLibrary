import braintree
import json
from django.http import HttpResponse
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework import mixins
from django.conf import settings
from authApi.models import shopCar, shopHistory, Book
from .serializers import cartSerializer
from .tasks import sent_transaction_mail


class brainTreePayment(ViewSet):
    if settings.DEBUG:
        # braintree_env = braintree.Environment.Production
        braintree_env = braintree.Environment.Sandbox
    else:
        braintree_env = braintree.Environment.Sandbox

    gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            braintree_env,
            merchant_id=settings.BRAINTREE_MERCHANT_ID,
            public_key=settings.BRAINTREE_PUBLIC_KEY,
            private_key=settings.BRAINTREE_PRIVATE_KEY
        )
    )

    def getClientToken(self, request):
        client_token = self.gateway.client_token.generate()
        # client_token = gateway.client_token.generate({
        #     "customer_id": a_customer_id
        # })
        return Response({'token': client_token})

    def createTransaction(self, request):
        nonce = request.data.get('nonce', None)
        amount = request.data.get('amount', 0)

        result = self.gateway.transaction.sale({
            "amount": str(amount),
            "payment_method_nonce": nonce,
            "options": {
                "submit_for_settlement": True
            }
        })

        if result.is_success:
            t = result.transaction

            books = request.data.get('books', None)

            if books:
                for book, quantity in json.loads(books).items():
                    h = shopHistory.objects.create(user=request.user,
                                                   book=Book.objects.get(
                                                       id=int(book)),
                                                   quantity=int(quantity),
                                                   transaction_id=str(t.id),
                                                   transaction_total_amount=t.amount,
                                                   transaction_currency=t.currency_iso_code,
                                                   transaction_pay_type=t.payment_instrument_type)
                    h.save()

            sent_transaction_mail.delay(
                t.id, request.user.username, request.user.email)

            return Response({'data': {
                'status': t.status,
                'transaction_id': t.id,
                'amount': t.amount,
                'currency': t.currency_iso_code,
                'date': t.created_at,
                'payment_type': t.payment_instrument_type,
            }})
        else:
            # print(result.errors.deep_errors)
            e = []
            for error in result.errors.deep_errors:
                e.append({
                    'cade': error.code,
                    'message': error.message
                })
            return Response({'data': e}, status=status.HTTP_400_BAD_REQUEST)


class shopCarManage(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):

    serializer_class = cartSerializer

    def list(self, request, *args, **kwargs):
        self.queryset = shopCar.objects.filter(
            user=self.request.user.id).exclude(quantity=0)
        return super(shopCarManage, self).list(request, *args, **kwargs)

    # def update(self, request, *args, **kwargs):
    #     books = self.request.data.get('book', [])

    #     shopCar.objects.filter(book__in=json.loads(books)).exclude(
    #         sold=True).update(sold=True, sold_date=timezone.now())

    #     instance = shopCar.objects.filter(book__in=json.loads(books)).values()

    #     return Response({'data': instance}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        action = self.request.query_params.get('del', 'one')
        if action == 'one':
            instance = shopCar.objects.filter(user=self.request.user.id).filter(
                book=request.data.get('book', 0))
        elif action == 'all':
            instance = shopCar.objects.filter(user=self.request.user.id)

        result = instance.delete()
        return Response({'data': {'delete_count': result[0]}}, status=status.HTTP_200_OK)
