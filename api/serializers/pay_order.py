from rest_framework import serializers
from api.models import payOrder, payOrderDetail, User
from .pay_order_detail import payOrderDetailSerializer


class payOrderSerializer(serializers.ModelSerializer):

    item_list = payOrderDetailSerializer(
        many=True, source='payorderdetail_set')

    def create(self, data):
        print(data)
        items_data = data.pop("payorderdetail_set", None)
        print(data)
        instance = payOrder.objects.create(
            user=User.objects.get(id=1),
            **data
        )

        for item_data in items_data:
            payOrderDetail.objects.create(
                pay_order=instance,
                **item_data
            )

        instance.save()

        return instance

    class Meta:
        model = payOrder
        fields = ['id', 'user', 'state', 'total_price',
                  'pay_type', 'create_date', 'item_list']
        read_only_fields = ('user',)
