# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-05-23 13:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0028_image_unique_image_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='unique_image_id',
            field=models.CharField(default=None, max_length=120, null=True, unique=True),
        ),
    ]
