# Generated by Django 5.0.1 on 2024-03-15 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_order_list_bought_options_receipt_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt_list',
            name='state',
            field=models.BooleanField(default=False, verbose_name='состояние'),
        ),
    ]