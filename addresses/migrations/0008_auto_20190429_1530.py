# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-04-29 15:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0007_address_address_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_type',
            field=models.CharField(blank=True, choices=[('billing', 'Billing address'), ('shipping', 'Shipping address')], max_length=120, null=True),
        ),
    ]
