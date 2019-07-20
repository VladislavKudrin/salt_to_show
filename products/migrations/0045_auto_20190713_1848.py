# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-07-13 18:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0044_auto_20190712_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='condition',
            field=models.CharField(choices=[('item condition', 'Select an item condition'), ('new with tags', 'New with tags'), ('gently used', 'Gently used'), ('used', 'Used')], default='not picked', max_length=120, null=True),
        ),
    ]
