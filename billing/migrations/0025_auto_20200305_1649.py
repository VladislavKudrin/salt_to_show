# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2020-03-05 16:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0024_auto_20200305_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingprofile',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=16, null=True),
        ),
    ]