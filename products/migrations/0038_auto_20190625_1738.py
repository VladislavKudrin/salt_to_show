# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-06-25 17:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0037_auto_20190624_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('select a category', 'Select a category'), ('tops', 'Tops'), ('bottoms', 'Bottoms'), ('accessories', 'Accessories'), ('outerwear', 'Outerwear'), ('footwear', 'Footwear')], default='all', max_length=120),
        ),
    ]
