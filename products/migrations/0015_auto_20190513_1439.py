# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-05-13 14:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0007_remove_size_size_test'),
        ('products', '0014_auto_20190513_0923'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.ManyToManyField(blank=True, null=True, to='categories.Size'),
        ),
    ]
