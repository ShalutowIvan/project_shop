# Generated by Django 4.2.3 on 2023-09-04 15:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_group', models.CharField(db_index=True, default='_', max_length=255, verbose_name='Название группы')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Группа',
                'verbose_name_plural': 'Группы',
                'ordering': ['name_group'],
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_org', models.CharField(default='_', max_length=255, verbose_name='Название организации')),
                ('inn_kpp', models.CharField(default='0', max_length=255, verbose_name='ИНН-КПП')),
                ('ogrn', models.IntegerField(default=0, verbose_name='ОГРН')),
                ('working_mode', models.CharField(default='_', max_length=255, verbose_name='Режим работы')),
                ('about', models.TextField(blank=True, verbose_name='О компании')),
                ('adres', models.CharField(default='_', max_length=255, verbose_name='Адрес организации')),
                ('phone', models.IntegerField(default=0, verbose_name='Телефон')),
                ('email_name', models.CharField(default='_', max_length=255, verbose_name='Электронная почта')),
                ('telegram', models.CharField(default='_', max_length=255, verbose_name='Контакты в Telegram')),
                ('whatsApp', models.CharField(default='_', max_length=255, verbose_name='Контакты в WhatsApp')),
            ],
            options={
                'verbose_name': 'Организация',
                'verbose_name_plural': 'Организация',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment', models.CharField(max_length=255, verbose_name='Способ оплаты')),
            ],
            options={
                'verbose_name': 'Способ оплаты',
                'verbose_name_plural': 'Способы оплаты',
            },
        ),
        migrations.CreateModel(
            name='Order_list_bought',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_product', models.CharField(default='_', max_length=255, verbose_name='Название товара')),
                ('price', models.DecimalField(decimal_places=2, max_digits=19, verbose_name='Цена')),
                ('quantity', models.FloatField(verbose_name='Количество')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='showcase.group', verbose_name='Группа товара')),
            ],
            options={
                'verbose_name': 'История покупок',
                'verbose_name_plural': 'История покупок',
                'ordering': ['time_create', 'name_product'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('fio', models.CharField(max_length=255, verbose_name='ФИО')),
                ('phone', models.IntegerField(default=0, verbose_name='Телефон')),
                ('e_mail', models.CharField(max_length=255, verbose_name='Электронная почта')),
                ('delivery_address', models.TextField(blank=True, verbose_name='Адрес доставки')),
                ('pay', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='showcase.payment', verbose_name='Способ оплаты')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['created_timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_product', models.CharField(default='_', max_length=255, verbose_name='Название товара')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('price', models.DecimalField(decimal_places=2, max_digits=19, verbose_name='Цена')),
                ('photo', models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото')),
                ('stock', models.FloatField(verbose_name='Остаток')),
                ('availability', models.BooleanField(default=True, verbose_name='Доступность')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='showcase.group', verbose_name='Группа товара')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ['stock', 'name_product'],
                'index_together': {('id', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='Baskets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=0, verbose_name='Количество')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('availability', models.BooleanField(default=True, verbose_name='Доступность')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=19, verbose_name='Цена')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='showcase.goods', verbose_name='Товар')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Товары в корзине',
                'verbose_name_plural': 'Товары в корзине',
                'ordering': ['product'],
            },
        ),
    ]
