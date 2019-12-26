# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-12-16 20:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0066_auto_20191216_2005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shipping_price',
            name='product',
        ),
        migrations.AddField(
            model_name='product',
            name='shipping_price',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product', to='products.Shipping_price'),
        ),
    ]
