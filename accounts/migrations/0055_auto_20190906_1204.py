# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-09-06 12:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0054_region_currency_mult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='currency_mult',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10, null=True),
        ),
    ]
