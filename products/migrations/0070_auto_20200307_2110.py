# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2020-03-07 21:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0069_auto_20200305_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=16),
        ),
    ]
