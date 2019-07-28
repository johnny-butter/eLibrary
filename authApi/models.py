from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.


class User(AbstractUser):
    email = models.CharField(unique=True, null=True, max_length=254)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []


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


class shopCar(models.Model):
    user = models.ForeignKey('User', models.CASCADE)
    book = models.ForeignKey('Book', models.CASCADE)
    quantity = models.IntegerField(default=1)
    create_date = models.DateTimeField(default=timezone.now())
    sold = models.BooleanField(default=False)
    sold_date = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = 'shop_car'
        unique_together = (("user", "book"),)


class shopHistory(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    book = models.ForeignKey('Book', models.DO_NOTHING)
    quantity = models.IntegerField()
    sold_date = models.DateTimeField(default=timezone.now())
    transaction_id = models.CharField(max_length=30)
    transaction_total_amount = models.DecimalField(
        max_digits=10, decimal_places=3)
    transaction_currency = models.CharField(max_length=5)
    transaction_pay_type = models.CharField(max_length=15)

    class Meta:
        db_table = 'shop_history'
        unique_together = (("book", "transaction_id"),)
