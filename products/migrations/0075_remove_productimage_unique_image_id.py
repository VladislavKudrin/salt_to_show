# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2020-04-01 15:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0074_auto_20200322_1750'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='unique_image_id',
        ),
    ]