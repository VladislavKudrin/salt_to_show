# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-12-16 16:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0062_auto_20191216_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='shipping_price',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shipping_price', to='products.Shipping_price'),
        ),
    ]
