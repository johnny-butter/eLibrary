from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from api.models import FavoriteBook


class BookFavSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteBook
        exclude = ('id', 'user')
        read_only_fields = ('isFavorite',)

    # avoid UniqueTogetherValidator fail cause by get_or_create
    def run_validators(self, value):
        for validator in self.validators.copy():
            if isinstance(validator, UniqueTogetherValidator):
                self.validators.remove(validator)

        super(BookFavSerializer, self).run_validators(value)

    def create(self, data):
        fav_book_data = {
            'book': data['book'],
            'user': self.context['request'].user,
            'defaults': {'isFavorite': True},
        }

        fav_book, created = FavoriteBook.objects.get_or_create(**fav_book_data)

        if not created:
            fav_book.isFavorite = not fav_book.isFavorite
            fav_book.save()

        return fav_book
