from django.db import models
from django.utils import timezone


class OauthRecord(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=32)
    create_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'api_oauth_record'

        indexes = [
            models.Index(fields=['user']),
        ]
