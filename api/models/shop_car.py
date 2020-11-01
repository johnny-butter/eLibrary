from django.db import models
from django.utils import timezone


class ShopCar(models.Model):
    user = models.ForeignKey('User', models.CASCADE)
    book = models.ForeignKey('Book', models.CASCADE)
    quantity = models.IntegerField(default=0)
    create_date = models.DateTimeField(default=timezone.now)
    sold = models.BooleanField(default=False)
    sold_date = models.DateTimeField(null=True, default=None)

    def add_quantity(self, amount=1):
        self.quantity += amount

    def cut_quantity(self, amount=1):
        self.quantity -= amount

        if self.quantity < 0:
            self.quantity = 0

    class Meta:
        db_table = 'shop_car'
        unique_together = (("user", "book"),)

        indexes = [
            models.Index(fields=['user', 'book']),
        ]
