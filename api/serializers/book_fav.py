from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from api.models import favoriteBook


class bookFavSerializer(serializers.ModelSerializer):
    class Meta:
        model = favoriteBook
        # fields = '__all__'
        exclude = ('id', 'user')
        read_only_fields = ('isFavorite',)
        # extra_kwargs = {
        #     'user': {'write_only': True},
        # }

    # avoid UniqueTogetherValidator fail cause by get_or_create
    def run_validators(self, value):
        for validator in self.validators.copy():
            if isinstance(validator, UniqueTogetherValidator):
                self.validators.remove(validator)

        super(bookFavSerializer, self).run_validators(value)

    def create(self, data):
        user = self.context['request'].user

        favorite, created = favoriteBook.objects.get_or_create(book=data['book'],
                                                               user=user,
                                                               defaults={'isFavorite': True})
        if not created:
            favorite.isFavorite = not favorite.isFavorite
            favorite.save()

        return favorite
