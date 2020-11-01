from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
from functools import wraps
from shared.errors import StockNotEnough


class Book(models.Model):
    name = models.CharField(max_length=30)
    type = models.ForeignKey('BookType', models.PROTECT)
    author = models.ForeignKey('Author', models.PROTECT, blank=True, null=True)
    publish_company = models.ForeignKey(
        'PublishCompany', models.PROTECT, blank=True, null=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    price_origin = models.IntegerField()
    price_discount = models.IntegerField(blank=True, null=True)
    stock = models.IntegerField(default=0)
    update_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'book'

    def add_stock(self, amount=1):
        self.stock += amount

    def cut_stock(self, amount=1):
        self.stock -= amount

        if self.stock < 0:
            self.stock = 0

    @staticmethod
    def check_stock(func):

        @wraps(func)
        def executor(view_set_instance, request, *args, **kwargs):
            if request.GET.get('action') == 'add':
                book = Book.objects.get(id=request.POST['book'])
                if book.stock < int(request.GET.get('amount', '1')):
                    raise StockNotEnough()

            return func(view_set_instance, request, *args, **kwargs)

        return executor


@receiver(pre_save, sender=Book)
def record_update_time(sender, instance, **kwargs):
    instance.update_at = timezone.now()
