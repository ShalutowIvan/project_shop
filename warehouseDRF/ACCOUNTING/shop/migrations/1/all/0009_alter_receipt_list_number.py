# Generated by Django 5.0.1 on 2024-03-16 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_alter_receipt_numbers_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt_list',
            name='number',
            field=models.IntegerField(default=0, verbose_name='Номер накладной'),
        ),
    ]
