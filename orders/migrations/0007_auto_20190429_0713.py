# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-04-29 07:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20190422_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='billing_address_final',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address_final',
            field=models.TextField(blank=True, null=True),
        ),
    ]
