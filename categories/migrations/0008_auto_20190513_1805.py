# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-05-13 18:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0007_remove_size_size_test'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TestSize',
        ),
        migrations.RemoveField(
            model_name='size',
            name='size_pants',
        ),
        migrations.RemoveField(
            model_name='size',
            name='size_shoes',
        ),
        migrations.RemoveField(
            model_name='size',
            name='size_tops',
        ),
        migrations.AddField(
            model_name='size',
            name='size',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='size',
            name='size_for',
            field=models.CharField(blank=True, max_length=120),
        ),
    ]