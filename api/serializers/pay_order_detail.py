from rest_framework import serializers
from api.models import payOrderDetail


class PayOrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = payOrderDetail
        exclude = ('id', 'pay_order')
