# Generated by Django 5.0.4 on 2024-06-25 09:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0019_alter_cart_cprice"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cart",
            old_name="cprice",
            new_name="ccprice",
        ),
    ]
