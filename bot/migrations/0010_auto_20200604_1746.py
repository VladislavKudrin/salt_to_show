# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2020-06-04 17:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0009_auto_20200515_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginmode',
            name='email',
            field=models.EmailField(blank=True, max_length=255),
        ),
    ]
