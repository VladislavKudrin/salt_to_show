# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-11-14 10:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_ecommerce', '0004_auto_20191031_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='buy_requested',
            field=models.BooleanField(default=False),
        ),
    ]