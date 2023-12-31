# Generated by Django 4.2.3 on 2023-08-11 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0002_alter_goods_group_alter_group_name_group_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods_in_basket',
            name='quantity',
            field=models.FloatField(default=0, verbose_name='Количество'),
        ),
        migrations.AlterIndexTogether(
            name='goods',
            index_together={('id', 'slug')},
        ),
    ]
