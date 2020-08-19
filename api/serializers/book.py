from rest_framework import serializers
from api.models import Book
from django.utils.translation import gettext_lazy as _


class bookSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(allow_null=True, source='type.name')
    author_name = serializers.CharField(allow_null=True, source='author.name')
    favthis = serializers.SerializerMethodField()
    i18n_test = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = (
            'id', 'name', 'type_name', 'author_name',
            'price_origin', 'price_discount', 'favthis',
            'i18n_test',
        )

    def get_favthis(self, obj):
        favQuery = self.context.get('favQuery')
        if favQuery:
            if obj.id in favQuery:
                return True
            else:
                return False

        return False
