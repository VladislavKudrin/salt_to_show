# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-09-10 12:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0025_auto_20190910_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='size',
            name='size_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='categories.Overcategory'),
        ),
    ]
