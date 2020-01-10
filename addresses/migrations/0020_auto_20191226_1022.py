# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-12-26 10:22
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0019_auto_20191226_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='name',
            field=models.CharField(blank=True, max_length=120, null=True, validators=[django.core.validators.RegexValidator("^[a-zA-Zа-яА-ЯҐЄІЇґєії\\'\\`\\’\\-\\. ]+$", 'Only letters and spaces are allowed'), django.core.validators.MinLengthValidator(6)]),
        ),
    ]
