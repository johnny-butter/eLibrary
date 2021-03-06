from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from api.models import ShopCar


class CartSerializer(serializers.ModelSerializer):
    book_name = serializers.CharField(read_only=True, source='book.name')
    book_price = serializers.CharField(
        read_only=True, source='book.price_discount')

    def run_validators(self, value):
        for validator in self.validators.copy():
            if isinstance(validator, UniqueTogetherValidator):
                self.validators.remove(validator)

        super(CartSerializer, self).run_validators(value)

    def create(self, data):
        user = self.context['request'].user
        cart, created = ShopCar.objects.get_or_create(user=user, book=data['book'])

        return cart

    class Meta:
        model = ShopCar
        exclude = ('id', 'user')
