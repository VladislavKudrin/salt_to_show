# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-09-06 12:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0053_auto_20190827_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='currency_mult',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
