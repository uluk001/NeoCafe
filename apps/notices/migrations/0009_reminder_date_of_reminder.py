# Generated by Django 4.2.7 on 2023-12-30 12:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("notices", "0008_reminder"),
    ]

    operations = [
        migrations.AddField(
            model_name="reminder",
            name="date_of_reminder",
            field=models.DateTimeField(auto_now_add=True, default='2023-12-26 07:03:31.713547'),
            preserve_default=False,
        ),
    ]