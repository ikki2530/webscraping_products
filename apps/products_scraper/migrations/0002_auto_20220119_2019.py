# Generated by Django 3.1.6 on 2022-01-19 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products_scraper', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='original_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='sale_price',
            field=models.FloatField(),
        ),
    ]