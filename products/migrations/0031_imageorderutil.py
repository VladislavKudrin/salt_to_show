# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-05-27 11:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0030_auto_20190524_1345'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageOrderUtil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, default=None, unique=True)),
                ('order_sequence', models.CharField(max_length=120)),
            ],
        ),
    ]