# Generated by Django 4.2.7 on 2023-12-04 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordering', '0002_remove_order_total_price_with_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='spent_bonus_points',
            field=models.PositiveIntegerField(default=0, verbose_name='Spent bonus points'),
        ),
    ]
