# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-09-06 13:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0059_auto_20190906_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=10),
        ),
    ]
