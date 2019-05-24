# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-05-13 14:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0007_remove_size_size_test'),
        ('products', '0015_auto_20190513_1439'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='categories.Size'),
        ),
    ]