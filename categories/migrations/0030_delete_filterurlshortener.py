# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2020-04-11 18:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0029_remove_filterurlshortener_main'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FilterUrlShortener',
        ),
    ]
