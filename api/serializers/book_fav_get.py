from rest_framework import serializers
from api.models import favoriteBook


class bookFavGetSerializer(serializers.ModelSerializer):
    bookinfo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = favoriteBook
        fields = ('bookname', 'bookinfo')

    def get_bookinfo(self, obj):
        dict = {'name': obj.bookname.name,
                'type_name': obj.bookname.type.name,
                'author_name': obj.bookname.author.name if obj.bookname.author else 'unknow',
                'price_origin': obj.bookname.price_origin,
                'price_discount': obj.bookname.price_discount}
        return dict
