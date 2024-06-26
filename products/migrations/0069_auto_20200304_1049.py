# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2020-03-04 10:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0068_auto_20200224_0321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='shipping_price',
        ),
        migrations.AddField(
            model_name='product',
            name='international_shipping',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=16),
        ),
        migrations.AddField(
            model_name='product',
            name='national_shipping',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=16),
        ),
        migrations.DeleteModel(
            name='Shipping_price',
        ),
    ]
