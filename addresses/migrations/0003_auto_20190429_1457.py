# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-04-29 14:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_auto_20190429_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='name',
            field=models.CharField(blank=True, help_text='Shipping to? Who is it for?', max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='nickname',
            field=models.CharField(blank=True, help_text='Internal Reference Nickname', max_length=120, null=True),
        ),
    ]
