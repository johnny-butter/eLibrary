from rest_framework import serializers
from api.models import shopHistory


class shopHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = shopHistory
        exclude = ('id', 'pay_order')
