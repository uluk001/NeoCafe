# Generated by Django 4.2.7 on 2023-11-28 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0013_remove_ingredient_minimal_limit_minimallimitreached'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='readymadeproduct',
            name='minimal_limit',
        ),
        migrations.AddField(
            model_name='minimallimitreached',
            name='ready_made_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='minimal_limit_reached', to='storage.readymadeproduct'),
        ),
        migrations.AlterField(
            model_name='minimallimitreached',
            name='ingredient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='minimal_limit_reached', to='storage.ingredient'),
        ),
    ]
