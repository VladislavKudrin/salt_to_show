# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-08-05 09:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0056_auto_20190802_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='authentic',
            field=models.CharField(choices=[('undefined', 'Undefined'), ('fake', 'Fake'), ('authentic', 'Authentic')], default='undefined', max_length=120, null=True),
        ),
    ]