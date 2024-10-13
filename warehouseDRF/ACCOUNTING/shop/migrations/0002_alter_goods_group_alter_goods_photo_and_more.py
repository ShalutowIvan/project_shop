# Generated by Django 5.0.1 on 2024-10-06 08:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='group',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='shop.group', verbose_name='Группа товара'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='photo',
            field=models.ImageField(default='_', upload_to='photos/%Y/%m/%d/', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='slug',
            field=models.SlugField(default='_', max_length=255, unique=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='stock',
            field=models.FloatField(default=0, verbose_name='Остаток'),
        ),
    ]