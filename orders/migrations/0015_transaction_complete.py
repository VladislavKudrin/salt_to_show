# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-12-24 20:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_auto_20191224_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]
