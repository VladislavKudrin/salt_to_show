# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-05-12 07:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_product_photos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='photos',
        ),
    ]
