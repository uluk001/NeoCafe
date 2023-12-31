# Generated by Django 4.2.7 on 2023-12-10 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("branches", "0008_alter_branch_schedule"),
        (
            "storage",
            "0017_alter_readymadeproductavailableatthebranch_ready_made_product",
        ),
        ("ordering", "0005_order_in_an_institution"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="branch",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to="branches.branch",
                verbose_name="Branch",
            ),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="ready_made_product",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="order_items",
                to="storage.readymadeproduct",
                verbose_name="Ready made product",
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="item",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="order_items",
                to="storage.item",
                verbose_name="Item",
            ),
        ),
    ]
