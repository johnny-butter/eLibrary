from rest_framework import serializers
from api.models import PayOrderDetail


class PayOrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = PayOrderDetail
        exclude = ('id', 'pay_order')
