from rest_framework import serializers
from api.models import User, Book, favoriteBook, shopCar, payOrder, payOrderDetail
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from django.utils.translation import gettext_lazy as _
import json


class userSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(
        required=True, allow_blank=False, max_length=100, min_length=5,
        validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(required=True, write_only=True)
    email = serializers.CharField(
        required=True, allow_null=True, max_length=100, validators=[UniqueValidator(queryset=User.objects.all())])
    is_staff = serializers.BooleanField(required=False, default=False)
    is_superuser = serializers.BooleanField(required=False, default=False)

    # def validate_username(self, value):
    #     if User.objects.filter(username=value).exists():
    #         raise serializers.ValidationError('The username has been used')

    def create(self, data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        instance = User.objects.create(
            username=data.get('username'),
            email=data.get('email'),
            is_staff=data.get('is_staff'),
            is_superuser=data.get('is_superuser'),
        )
        instance.set_password(data.get('password'))
        instance.save()
        return instance

    def update(self, instance, data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.username = data.get('username', instance.username)
        instance.email = data.get('email', instance.email)
        instance.is_staff = data.get('is_staff', instance.is_staff)
        instance.is_superuser = data.get('is_superuser', instance.is_staff)
        if not data.get('password', None) == 'NOT_UPDATE':
            instance.set_password(data.get('password'))
        instance.save()
        return instance


class bookFavSerializer(serializers.ModelSerializer):
    class Meta:
        model = favoriteBook
        # fields = '__all__'
        exclude = ('id',)
        read_only_fields = ('isFavorite',)
        extra_kwargs = {
            'username': {'write_only': True},
        }

    # Avoid UniqueTogetherValidator fail, cause can't use get_or_create
    def run_validators(self, value):
        for validator in self.validators.copy():
            if isinstance(validator, UniqueTogetherValidator):
                self.validators.remove(validator)
        super(bookFavSerializer, self).run_validators(value)

    def create(self, data):
        favorite, created = favoriteBook.objects.get_or_create(bookname=data['bookname'],
                                                               username=data['username'],
                                                               defaults={'isFavorite': True})
        if not created:
            favorite.isFavorite = not favorite.isFavorite
            favorite.save()

        return favorite


class bookFavGetSerializer(serializers.ModelSerializer):
    bookinfo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = favoriteBook
        fields = ('bookname', 'bookinfo')

    def get_bookinfo(self, obj):
        # print(obj)
        dict = {'name': obj.bookname.name,
                'type_name': obj.bookname.type.name,
                'author_name': obj.bookname.author.name if obj.bookname.author else 'unknow',
                'price_origin': obj.bookname.price_origin,
                'price_discount': obj.bookname.price_discount}
        return dict


class bookSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(allow_null=True, source='type.name')
    author_name = serializers.CharField(allow_null=True, source='author.name')
    favthis = serializers.SerializerMethodField()
    i18n_test = serializers.SerializerMethodField()
    # favoritebook_set = bookFavSerializer(many=True)

    class Meta:
        model = Book
        fields = ('id', 'name', 'type_name', 'author_name',
                  'price_origin', 'price_discount', 'favthis', 'i18n_test')

    def get_favthis(self, obj):
        favQuery = self.context.get('favQuery')
        if favQuery:
            if obj.id in favQuery:
                return True
            else:
                return False
        return False

    def get_i18n_test(self, obj):
        return _('hello world')


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
        action = self.context['request'].query_params.get('action', 'add')
        cart, created = shopCar.objects.get_or_create(user=self.context['request'].user,
                                                      book=data['book'])
        if not created:
            if action == 'add':
                cart.quantity += 1
            elif action == 'cut':
                cart.quantity = cart.quantity - 1 if cart.quantity > 0 else 0

            cart.save()

        return cart

    class Meta:
        model = shopCar
        exclude = ('id', 'user')
        # fields = '__all__'


class payOrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = payOrderDetail
        exclude = ('id', 'pay_order')


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


# {"total_price": 500, "pay_type": "braintree", "item_list": [{"quantity": 1, "price": 100, "book": 2}, {"quantity": 5, "price": 500, "book": 3}, {"quantity": 7, "price": 700, "book": 5}]}
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
