from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from api.models import favoriteBook


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
