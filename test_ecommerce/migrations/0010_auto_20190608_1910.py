# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-06-08 19:10
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_ecommerce', '0009_auto_20190531_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='example',
            name='input_file',
            field=models.FileField(max_length=255, storage=django.core.files.storage.FileSystemStorage(location='/Users/roma/Dev/market/marketplace/live-static-files/media-root'), upload_to='example'),
        ),
        migrations.AlterField(
            model_name='examplefile',
            name='input_file',
            field=models.FileField(max_length=255, storage=django.core.files.storage.FileSystemStorage(location='/Users/roma/Dev/market/marketplace/live-static-files/media-root'), upload_to='example'),
        ),
    ]
