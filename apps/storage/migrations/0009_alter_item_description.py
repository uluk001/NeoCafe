# Generated by Django 4.2.7 on 2023-11-18 16:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("storage", "0008_readymadeproduct_date_of_arrival"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]
