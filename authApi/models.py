from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django_fsm import FSMIntegerField, FSMField, transition
from error_code import PayFail

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

    def __str__(self):
        return self.name

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
    pay_order = models.ForeignKey('payOrder', models.DO_NOTHING)
    transaction_id = models.CharField(max_length=30)
    transaction_total_price = models.DecimalField(
        max_digits=10, decimal_places=3)
    transaction_currency = models.CharField(max_length=5)
    transaction_pay_type = models.CharField(max_length=15)
    create_date = models.DateTimeField(default=timezone.now())

    class Meta:
        db_table = 'shop_history'


class payOrderStateEnum:
    PENDING = 0
    PAID = 1
    SHIPPING = 2
    ARRIVED = 3
    RETURNED = 4
    REFUNDED = 5


class payOrder(models.Model):
    user = models.ForeignKey('User', models.CASCADE)
    state = FSMIntegerField(default=payOrderStateEnum.PENDING)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=3)
    pay_type = models.CharField(max_length=30)
    create_date = models.DateTimeField(default=timezone.now())

    class Meta:
        db_table = 'pay_order'

    @transition(field=state, source=payOrderStateEnum.PENDING, target=payOrderStateEnum.PAID)
    def pay(self, pay_method='braintree', braintree_gateway=None, braintree_nonce=None):
        if pay_method == 'braintree':
            result = braintree_gateway.transaction.sale({
                "amount": str(self.total_price),
                "payment_method_nonce": braintree_nonce,
                "options": {
                    "submit_for_settlement": True
                }
            })
            if result.is_success:
                return self, result
            else:
                e = []
                for error in result.errors.deep_errors:
                    e.append({
                        'cade': error.code,
                        'message': error.message
                    })
                raise PayFail(detail={'detail': e})


class payOrderDetail(models.Model):
    pay_order = models.ForeignKey('payOrder', models.DO_NOTHING)
    book = models.ForeignKey('Book', models.DO_NOTHING)
    quantity = models.IntegerField()
    price = models.DecimalField(
        max_digits=10, decimal_places=3)
    create_date = models.DateTimeField(default=timezone.now())

    class Meta:
        db_table = 'pay_order_detail'
