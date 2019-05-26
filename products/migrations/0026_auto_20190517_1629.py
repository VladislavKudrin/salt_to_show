# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-05-17 16:29
from __future__ import unicode_literals

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0025_auto_20190517_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, height_field='height', null=True, upload_to=products.models.upload_image_path, width_field='width'),
        ),
    ]