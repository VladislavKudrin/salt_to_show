# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-05-10 07:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0026_auto_20190510_0747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]
