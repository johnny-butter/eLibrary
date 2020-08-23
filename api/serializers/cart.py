from rest_framework import serializers
from api.models import shopCar
from rest_framework.validators import UniqueTogetherValidator
from django.utils.translation import gettext_lazy as _


class cartSerializer(serializers.ModelSerializer):
    book_name = serializers.CharField(read_only=True, source='book.name')
    book_price = serializers.CharField(
        read_only=True, source='book.price_discount')

    def run_validators(self, value):
        for validator in self.validators.copy():
            if isinstance(validator, UniqueTogetherValidator):
                self.validators.remove(validator)
        super(cartSerializer, self).run_validators(value)

    def create(self, data):
        cart, created = shopCar.objects.get_or_create(
            user=self.context['request'].user,
            book=data['book']
        )

        return cart

    class Meta:
        model = shopCar
        exclude = ('id', 'user')
