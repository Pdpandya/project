# Generated by Django 5.0.6 on 2024-06-24 14:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0014_cart_payment"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="cprice",
            field=models.PositiveIntegerField(default=""),
        ),
        migrations.AddField(
            model_name="cart",
            name="cqty",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name="cart",
            name="tprice",
            field=models.PositiveIntegerField(default=""),
        ),
    ]
