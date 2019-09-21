from django.db import models


class bookType(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'book_type'
