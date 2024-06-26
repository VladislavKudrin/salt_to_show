# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-12-08 16:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0008_auto_20190424_1647'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='active',
        ),
        migrations.RemoveField(
            model_name='card',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='card',
            name='country',
        ),
        migrations.RemoveField(
            model_name='card',
            name='default',
        ),
        migrations.RemoveField(
            model_name='card',
            name='last4',
        ),
        migrations.RemoveField(
            model_name='card',
            name='stripe_id',
        ),
        migrations.AddField(
            model_name='card',
            name='holder',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='card',
            name='number',
            field=models.IntegerField(blank=True, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='exp_month',
            field=models.IntegerField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='exp_year',
            field=models.IntegerField(blank=True, max_length=2, null=True),
        ),
    ]
