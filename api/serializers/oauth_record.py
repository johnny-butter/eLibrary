from rest_framework import serializers
from api.models import OauthRecord


class OauthRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = OauthRecord
        exclude = ('id', 'user')

    def create(self, data):
        instance = OauthRecord.objects.create(
            user=data['user'],
            provider=data['provider'],
            uid=data['uid']
        )

        return instance
