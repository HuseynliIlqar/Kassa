# Generated by Django 5.2.2 on 2025-07-06 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashDesk', '0005_remove_cartitem_cart_remove_cartitem_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='is_cart',
            field=models.BooleanField(default=True),
        ),
    ]
