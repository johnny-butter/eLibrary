from rest_framework import serializers
from api.models import PayOrder, PayOrderDetail
from api.serializers import PayOrderDetailSerializer


class PayOrderSerializer(serializers.ModelSerializer):

    item_list = PayOrderDetailSerializer(
        many=True, source='payorderdetail_set')

    def create(self, data):
        items_data = data.pop('payorderdetail_set', None)
        user = self.context['request'].user

        instance = PayOrder.objects.create(
            user=user,
            **data
        )

        PayOrderDetail.objects.bulk_create([
            PayOrderDetail(
                pay_order=instance,
                **item_data
            )
            for item_data in items_data
        ])

        return instance

    class Meta:
        model = PayOrder
        fields = ['id', 'user', 'state', 'total_price',
                  'pay_type', 'create_date', 'item_list']
        read_only_fields = ('user',)
