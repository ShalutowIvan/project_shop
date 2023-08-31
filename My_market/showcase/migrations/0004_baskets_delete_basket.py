# Generated by Django 4.2.3 on 2023-08-31 06:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('showcase', '0003_rename_goods_in_basket_basket'),
    ]

    operations = [
        migrations.CreateModel(
            name='Baskets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=0, verbose_name='Количество')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('availability', models.BooleanField(default=True, verbose_name='Доступность')),
                ('price', models.DecimalField(decimal_places=2, max_digits=19, verbose_name='Цена')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='showcase.goods', verbose_name='Товар')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Товары в корзине',
                'verbose_name_plural': 'Товары в корзине',
                'ordering': ['-price', 'product'],
            },
        ),
        migrations.DeleteModel(
            name='Basket',
        ),
    ]
