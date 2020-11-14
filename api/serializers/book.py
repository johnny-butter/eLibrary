from rest_framework import serializers
from api.models import Book
from django.utils.translation import gettext_lazy as _


class BookSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(allow_null=True, source='type.name')
    author_name = serializers.CharField(allow_null=True, source='author.name')
    is_fav = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = (
            'id', 'name', 'type_name', 'author_name',
            'price_origin', 'price_discount', 'is_fav',
            'stock', 'is_vip_only',
        )

    def get_is_fav(self, obj):
        fav_books = self.context.get('fav_books')

        if not fav_books:
            return False

        return obj.id in fav_books
