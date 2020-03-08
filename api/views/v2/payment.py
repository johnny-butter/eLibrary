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

    def createPayment(self, request):
        pay_order_id = request.data['pay_order_id']
        extra_data = request.data.get('extra_data', None)

        pay_order = payOrder.objects.get(id=pay_order_id)
        pay_order.pay(**extra_data)
        pay_order.save()

        shop_history = pay_order.shophistory_set.last()
        serializer = shopHistorySerializer(shop_history)

        return Response(serializer.data)
