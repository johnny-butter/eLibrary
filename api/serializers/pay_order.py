from rest_framework import serializers
from api.models import payOrder, payOrderDetail
from .pay_order_detail import payOrderDetailSerializer


class payOrderSerializer(serializers.ModelSerializer):

    item_list = payOrderDetailSerializer(
        many=True, source='payorderdetail_set')

    def create(self, data):
        items_data = data.pop('payorderdetail_set', None)
        user = self.context['request'].user

        instance = payOrder.objects.create(
            user=user,
            **data
        )

        for item_data in items_data:
            payOrderDetail.objects.create(
                pay_order=instance,
                **item_data
            )

        return instance

    class Meta:
        model = payOrder
        fields = ['id', 'user', 'state', 'total_price',
                  'pay_type', 'create_date', 'item_list']
        read_only_fields = ('user',)
