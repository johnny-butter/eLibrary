from rest_framework import serializers
from api.models import oauthRecord


class oauthRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = oauthRecord
        exclude = ('id', 'user')

    def create(self, data):
        instance = oauthRecord.objects.create(
            user=data['user'],
            provider=data['provider'],
            uid=data['uid']
        )

        return instance
