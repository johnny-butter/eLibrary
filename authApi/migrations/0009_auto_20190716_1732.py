# Generated by Django 2.2 on 2019-07-16 09:32

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authApi', '0008_shopcar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopcar',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 16, 9, 32, 28, 798074, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='shopHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('sold_date', models.DateTimeField(default=datetime.datetime(2019, 7, 16, 9, 32, 28, 798074, tzinfo=utc))),
                ('transaction_id', models.CharField(max_length=30)),
                ('transaction_total_amount', models.DecimalField(decimal_places=3, max_digits=10)),
                ('transaction_currency', models.CharField(max_length=5)),
                ('transaction_pay_type', models.CharField(max_length=15)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='authApi.Book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'shop_history',
                'unique_together': {('book', 'transaction_id')},
            },
        ),
    ]
