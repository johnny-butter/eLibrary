# Generated by Django 2.2 on 2020-11-14 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20200907_0544'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_vip_only',
            field=models.BooleanField(default=False),
        ),
    ]
