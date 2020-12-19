import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api.models import PayOrder
from api.models.pay_order import PayError
from api.serializers import PayOrderSerializer, ShopHistorySerializer
# from api.tasks import sent_shopping_record_mail
from api.kafka_tasks import order_paid_notify

from django_fsm import can_proceed

from shared.errors import ApiCheckFail, PayFail


class Payment(ViewSet):

    def get_pay_order_list(self, request):
        query_set = request.user.payorder_set.filter(state=0).first()

        if not query_set:
            raise ApiCheckFail()

        serializer = PayOrderSerializer(query_set)
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

        pay_order = PayOrder.objects.get(id=pay_order_id)

        try:
            pay_order.pay(**extra_data)
        except PayError as e:
            raise PayFail(detail=e.error_detail)

        pay_order.save()

        shop_history = pay_order.shophistory_set.last()
        serializer = ShopHistorySerializer(shop_history)

        # sent_shopping_record_mail.delay(pay_order.id)
        order_paid_notify(json.dumps({
            'pay_order_id': pay_order.id
        }))

        return Response(serializer.data)

    def cancel_pay_order(self, request):
        pay_order = PayOrder.objects.get(id=request.data['pay_order_id'])

        if not can_proceed(pay_order.cancel):
            raise ApiCheckFail("The state can't be canceled")

        pay_order.cancel()
        pay_order.save()

        return Response({'data': {'status': 'success'}})
