# Generated by Django 5.0.1 on 2024-10-23 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_inventory_buffer'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory_number',
            name='number_group',
            field=models.IntegerField(default=0, verbose_name='Номер группы'),
        ),
    ]
