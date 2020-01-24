from rest_framework import serializers
from api.models import favoriteBook


class bookFavGetSerializer(serializers.ModelSerializer):
    bookinfo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = favoriteBook
        fields = ('book', 'bookinfo')

    def get_bookinfo(self, obj):
        dict = {'name': obj.book.name,
                'type_name': obj.book.type.name,
                'author_name': obj.book.author.name if obj.book.author else 'unknow',
                'price_origin': obj.book.price_origin,
                'price_discount': obj.book.price_discount}

        return dict
