# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2020-04-06 14:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0061_delete_guestemail'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, max_length=155, null=True),
        ),
    ]