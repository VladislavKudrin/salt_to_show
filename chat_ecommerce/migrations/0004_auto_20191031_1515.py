# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-10-31 15:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0061_auto_20190906_1343'),
        ('chat_ecommerce', '0003_auto_20190615_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='thread',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Product'),
        ),
    ]