# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-09-10 12:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0024_auto_20190910_1201'),
    ]

    operations = [
        migrations.RenameField(
            model_name='size',
            old_name='size_kidss',
            new_name='size_kids',
        ),
    ]
