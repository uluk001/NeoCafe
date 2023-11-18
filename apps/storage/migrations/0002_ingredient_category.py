# Generated by Django 4.2.7 on 2023-11-11 11:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("storage", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="ingredient",
            name="category",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="storage.category",
            ),
            preserve_default=False,
        ),
    ]