# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-07-23 17:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0047_auto_20190723_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=600),
        ),
    ]
