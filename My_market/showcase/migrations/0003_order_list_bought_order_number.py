# Generated by Django 4.2.3 on 2023-09-12 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0002_remove_baskets_availability_remove_baskets_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_list_bought',
            name='order_number',
            field=models.IntegerField(default=0, verbose_name='Количество'),
        ),
    ]