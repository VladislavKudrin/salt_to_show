# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-07-20 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0012_auto_20190720_1803'),
    ]

    operations = [
        migrations.RenameField(
            model_name='overcategory',
            old_name='undercategory',
            new_name='overcategory',
        ),
        migrations.RemoveField(
            model_name='overcategory',
            name='undercategory_for',
        ),
        migrations.AddField(
            model_name='overcategory',
            name='overcategory_for',
            field=models.CharField(blank=True, max_length=120),
        ),
    ]
