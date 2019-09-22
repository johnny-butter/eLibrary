from rest_framework import serializers
from api.models import payOrderDetail


class payOrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = payOrderDetail
        exclude = ('id', 'pay_order')
