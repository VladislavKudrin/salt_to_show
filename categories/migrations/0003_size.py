# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-05-13 09:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0002_auto_20190511_1240'),
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size_pants', models.CharField(max_length=120)),
                ('size_shoes', models.CharField(max_length=120)),
                ('size_tops', models.CharField(max_length=120)),
            ],
        ),
    ]