# Generated by Django 3.2 on 2021-06-18 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0018_statistics_items_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ice_cream',
            name='active',
        ),
        migrations.RemoveField(
            model_name='ice_cream',
            name='inventory',
        ),
    ]
