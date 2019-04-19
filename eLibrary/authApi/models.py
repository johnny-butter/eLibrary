from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    pass


class Book(models.Model):
    name = models.CharField(max_length=30)
    type = models.ForeignKey('bookType', models.PROTECT)
    author = models.ForeignKey('Author', models.PROTECT, blank=True, null=True)
    publish_company = models.ForeignKey(
        'publishCompany', models.PROTECT, blank=True, null=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    price_origin = models.IntegerField()
    price_discount = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'book'


class Author(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'author'


class publishCompany(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'publish_company'


class bookType(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'book_type'


class favoriteBook(models.Model):
    bookname = models.ForeignKey('Book', models.PROTECT)
    username = models.ForeignKey('User', models.PROTECT)
    isFavorite = models.BooleanField()

    class Meta:
        db_table = 'favorite_book'
        unique_together = (("bookname", "username"),)
