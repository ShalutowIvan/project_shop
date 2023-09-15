# Generated by Django 4.2.3 on 2023-09-15 10:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('showcase', '0002_remove_baskets_availability_remove_baskets_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacts',
            name='user',
            field=models.ForeignKey(default='_', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
