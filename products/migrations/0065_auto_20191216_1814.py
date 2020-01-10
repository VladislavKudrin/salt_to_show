# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-12-16 18:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0064_auto_20191216_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='shipping_price',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product', to='products.Shipping_price'),
        ),
    ]
