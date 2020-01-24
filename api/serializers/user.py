from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from api.models import User


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
        if data.get('password', None):
            instance.set_password(data.get('password'))

        instance.save()

        return instance
