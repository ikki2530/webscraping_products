# Generated by Django 3.1.6 on 2022-01-19 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('original_price', models.IntegerField()),
                ('sale_price', models.IntegerField()),
                ('date', models.DateField()),
                ('date_auto', models.DateField(auto_now=True)),
            ],
        ),
    ]
