# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-05-06 12:39
from __future__ import unicode_literals

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20190506_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_foto',
            field=models.ImageField(blank=True, null=True, upload_to=accounts.models.upload_image_path),
        ),
    ]
