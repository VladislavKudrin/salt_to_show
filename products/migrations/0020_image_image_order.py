# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-05-17 12:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_merge_20190515_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='image_order',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=20),
        ),
    ]
