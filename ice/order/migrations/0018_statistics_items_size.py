# Generated by Django 3.2 on 2021-06-11 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0017_statistics_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistics',
            name='items_size',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
