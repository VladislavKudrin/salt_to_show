# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-07-28 17:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0018_auto_20190726_1043'),
    ]

    operations = [
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition', models.CharField(blank=True, max_length=120)),
                ('condition_ru', models.CharField(blank=True, max_length=120)),
                ('condition_ua', models.CharField(blank=True, max_length=120)),
            ],
        ),
    ]
