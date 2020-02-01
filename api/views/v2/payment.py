from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from api.models import shopHistory, payOrder
from api.serializers import payOrderSerializer, shopHistorySerializer


class payment(ViewSet):

    def getPayOrderList(self, request):
        query_set = request.user.payorder_set.filter(state=0)
        serializer = payOrderSerializer(query_set, many=True)
        resp = {
            'data': serializer.data,
        }

        return Response(resp)

    def createPayOrder(self, request):
        context = {'request': request}
        serializer = payOrderSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def createTransaction(self, request):
        pay_order_id = request.data['pay_order_id']
        extra_data = request.data.get('extra_data', None)

        pay_order = payOrder.objects.get(id=pay_order_id)

        instance, result = pay_order.pay(**extra_data)

        instance.save()

        if result.is_success:
            t = result.transaction

            shop_history = shopHistory.objects.create(
                pay_order=payOrder.objects.get(id=pay_order_id),
                transaction_id=str(t.id),
                transaction_total_price=t.amount,
                transaction_currency=t.currency_iso_code,
                transaction_pay_type=t.payment_instrument_type
            )

            serializer = shopHistorySerializer(shop_history)

            return Response(serializer.data)
