# Generated by Django 5.0.1 on 2024-03-16 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_receipt_list_number_receipt'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='receipt_list',
            options={'ordering': ['product'], 'verbose_name': 'Список приходных документов', 'verbose_name_plural': 'Списки приходных документов'},
        ),
        migrations.RemoveField(
            model_name='receipt_list',
            name='time_create',
        ),
    ]
