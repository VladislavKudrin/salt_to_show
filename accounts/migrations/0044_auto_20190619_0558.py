# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-06-19 05:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0043_auto_20190618_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='languagepreference',
            name='language',
            field=models.CharField(choices=[('RU', 'RU'), ('UA', 'UA'), ('EN', 'EN')], default='en', max_length=120),
        ),
    ]
