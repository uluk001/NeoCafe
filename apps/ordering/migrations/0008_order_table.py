# Generated by Django 4.2.7 on 2023-12-21 08:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ordering", "0007_alter_order_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="table",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Table number"
            ),
        ),
    ]
