from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet

from api.models import payOrder
from api.serializers import PayOrderSerializer, ShopHistorySerializer
from api.tasks import sent_shopping_record_mail


class Payment(ViewSet):

    def get_pay_order_list(self, request):
        query_set = request.user.payorder_set.filter(state=0)
        serializer = PayOrderSerializer(query_set, many=True)
        resp = {
            'data': serializer.data,
        }

        return Response(resp)

    def create_pay_order(self, request):
        context = {'request': request}
        serializer = PayOrderSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create_payment(self, request):
        pay_order_id = request.data['pay_order_id']
        extra_data = request.data.get('extra_data', None)

        pay_order = payOrder.objects.get(id=pay_order_id)
        pay_order.pay(**extra_data)
        pay_order.save()

        shop_history = pay_order.shophistory_set.last()
        serializer = ShopHistorySerializer(shop_history)

        sent_shopping_record_mail.delay(pay_order.id)

        return Response(serializer.data)
