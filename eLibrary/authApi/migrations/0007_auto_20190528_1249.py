# Generated by Django 2.2 on 2019-05-28 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authApi', '0006_auto_20190528_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=254, null=True, unique=True),
        ),
    ]
