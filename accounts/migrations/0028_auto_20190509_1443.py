# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-05-09 14:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_auto_20190509_0745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='wishes',
            field=models.ManyToManyField(related_name='users', to='products.Product'),
        ),
    ]
