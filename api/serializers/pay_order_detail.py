from rest_framework import serializers
from api.models import PayOrderDetail


class PayOrderDetailSerializer(serializers.ModelSerializer):

    book_name = serializers.CharField(read_only=True, source='book.name')

    class Meta:
        model = PayOrderDetail
        exclude = ('id', 'pay_order')
