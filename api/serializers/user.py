from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from api.models import User, oauthRecord
from .oauth_record import oauthRecordSerializer


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(
        required=True, allow_blank=False, max_length=100, min_length=5,
        validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(required=True, write_only=True)
    email = serializers.CharField(
        required=True, allow_null=True, max_length=100, validators=[UniqueValidator(queryset=User.objects.all())])
    is_staff = serializers.BooleanField(required=False, default=False)
    is_superuser = serializers.BooleanField(required=False, default=False)
    oauth_record = oauthRecordSerializer(required=False)

    class Meta:
        extra_kwargs = {
            'oauth_record': {'write_only': True},
        }

    def create(self, data):
        oauth_record_data = data.get('oauth_record', {})

        instance = User.objects.create(
            username=data.get('username'),
            email=data.get('email'),
            is_staff=data.get('is_staff'),
            is_superuser=data.get('is_superuser'),
        )
        instance.set_password(data.get('password'))

        instance.save()

        if oauth_record_data.get('provider', None):
            oauthRecord.objects.create(
                user=instance,
                **oauth_record_data
            )

        return instance

    def update(self, instance, data):
        instance.username = data.get('username', instance.username)
        instance.email = data.get('email', instance.email)
        instance.is_staff = data.get('is_staff', instance.is_staff)
        instance.is_superuser = data.get('is_superuser', instance.is_staff)
        if data.get('password', None):
            instance.set_password(data.get('password'))

        instance.save()

        return instance
