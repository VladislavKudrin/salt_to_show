# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-08-07 17:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0051_auto_20190807_1738'),
        ('analitics', '0003_regionpreference'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='regionpreference',
            name='user',
        ),
        migrations.DeleteModel(
            name='RegionPreference',
        ),
    ]