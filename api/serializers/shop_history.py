from rest_framework import serializers
from api.models import ShopHistory


class ShopHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ShopHistory
        exclude = ('id', 'pay_order')
