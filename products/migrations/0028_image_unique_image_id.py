# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-05-23 13:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0027_auto_20190517_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='unique_image_id',
            field=models.CharField(blank=True, default=None, max_length=120, null=True, unique=True),
        ),
    ]
