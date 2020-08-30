from rest_framework import serializers
from api.models import favoriteBook


class BookFavGetSerializer(serializers.ModelSerializer):
    book_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = favoriteBook
        fields = ('book', 'book_info')

    def get_book_info(self, obj):
        return {
            'name': obj.book.name,
            'type_name': obj.book.type.name,
            'author_name': obj.book.author.name if obj.book.author else 'unknow',
            'price_origin': obj.book.price_origin,
            'price_discount': obj.book.price_discount
        }
