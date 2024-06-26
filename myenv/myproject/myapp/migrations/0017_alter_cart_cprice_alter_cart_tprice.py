# Generated by Django 5.0.6 on 2024-06-24 16:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0016_alter_cart_cprice"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="cprice",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name="cart",
            name="tprice",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
