import braintree
import json
from django.http import HttpResponse
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework import mixins
from django.conf import settings
from api.models import shopCar, shopHistory, Book, payOrder, User
from .serializers import cartSerializer, payOrderSerializer
from .tasks import sent_transaction_mail
from django_fsm import can_proceed


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

        return Response({'token': client_token})

    def getPayOrderList(self, request):
        query_set = payOrder.objects.filter(
            user=User.objects.get(id=1), state=0)

        serializer = payOrderSerializer(query_set, many=True)
        return Response({'data': serializer.data})

    def createPayOrder(self, request):
        print(request.data)

        serializer = payOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def createTransaction(self, request):
        pay_order_id = request.data.get('pay_order_id', None)
        nonce = request.data.get('nonce', None)

        instance, result = payOrder.objects.get(id=pay_order_id).pay(
            pay_method='braintree',
            braintree_gateway=self.gateway,
            braintree_nonce=nonce
        )

        instance.save()

        if result.is_success:
            t = result.transaction

            h = shopHistory.objects.create(
                pay_order=payOrder.objects.get(id=pay_order_id),
                transaction_id=str(t.id),
                transaction_total_price=t.amount,
                transaction_currency=t.currency_iso_code,
                transaction_pay_type=t.payment_instrument_type
            )
            h.save()

            data = dict(
                status=t.status,
                transaction_id=t.id,
                amount=t.amount,
                currency=t.currency_iso_code,
                date=t.created_at,
                payment_type=t.payment_instrument_type,
            )
            return Response({'data': data})
        # else:
        #     return Response({'data': 'pay fail'}, status=status.HTTP_400_BAD_REQUEST)


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
