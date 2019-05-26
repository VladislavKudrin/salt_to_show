# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-05-17 16:26
from __future__ import unicode_literals

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_auto_20190517_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='height',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='image',
            name='width',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, height_field='heigth', null=True, upload_to=products.models.upload_image_path, width_field='width'),
        ),
    ]