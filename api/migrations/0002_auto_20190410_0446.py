# Generated by Django 2.1.2 on 2019-04-09 20:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'author',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('publish_date', models.DateTimeField()),
                ('price_origin', models.IntegerField()),
                ('price_discount', models.IntegerField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.Author')),
            ],
            options={
                'db_table': 'book',
            },
        ),
        migrations.CreateModel(
            name='bookType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'book_type',
            },
        ),
        migrations.CreateModel(
            name='publishCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'publish_company',
            },
        ),
        migrations.AddField(
            model_name='book',
            name='publish_company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.publishCompany'),
        ),
        migrations.AddField(
            model_name='book',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.bookType'),
        ),
    ]