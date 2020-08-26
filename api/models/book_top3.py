from django.db import models


class BookTop3(models.Model):
    book = models.ForeignKey('Book', models.PROTECT)
    book_count = models.IntegerField()
    count_time = models.CharField(max_length=20)

    def __str__(self):
        return self.book

    class Meta:
        db_table = 'book_top3'

        indexes = [
            models.Index(fields=['book']),
            models.Index(fields=['count_time']),
        ]
