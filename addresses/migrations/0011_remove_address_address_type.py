# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-04-29 15:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0010_auto_20190429_1540'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='address_type',
        ),
    ]
