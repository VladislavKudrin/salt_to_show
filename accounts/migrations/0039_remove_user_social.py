# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-05-28 09:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0038_user_social'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='social',
        ),
    ]
