# Generated by Django 5.0.1 on 2024-03-15 01:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_delete_url_list_alter_order_list_bought_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order_list_bought',
            options={'ordering': ['time_create', 'product_id'], 'verbose_name': 'Список заказов', 'verbose_name_plural': 'Списки заказов'},
        ),
        migrations.CreateModel(
            name='Receipt_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.FloatField(default=0, verbose_name='Количество')),
                ('state', models.BooleanField(default=True, verbose_name='состояние')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.goods', verbose_name='Товар')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Список приходных документов',
                'verbose_name_plural': 'Списки приходных документов',
                'ordering': ['time_create', 'product'],
            },
        ),
    ]