# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-05-10 07:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_product_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sex',
            field=models.CharField(choices=[('man', 'Man'), ('woman', 'Woman'), ('unisex', 'Unisex')], default='not picked', max_length=120),
        ),
    ]
