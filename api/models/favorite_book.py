from django.db import models


class favoriteBook(models.Model):
    bookname = models.ForeignKey('Book', models.PROTECT)
    username = models.ForeignKey('User', models.PROTECT)
    isFavorite = models.BooleanField()

    class Meta:
        db_table = 'favorite_book'
        unique_together = (("bookname", "username"),)
