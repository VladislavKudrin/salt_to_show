# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-05-06 14:25
from __future__ import unicode_literals

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_remove_profile_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.AddField(
            model_name='user',
            name='profile_foto',
            field=models.ImageField(blank=True, null=True, upload_to=accounts.models.upload_image_path),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
