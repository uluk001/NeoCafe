# Generated by Django 4.2.7 on 2023-12-04 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordering', '0003_order_spent_bonus_points'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='total_price',
        ),
    ]