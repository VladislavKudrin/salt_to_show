# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2020-04-01 15:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('file_id', models.CharField(blank=True, max_length=40, null=True)),
                ('form_id', models.CharField(blank=True, max_length=40, null=True)),
            ],
        ),
    ]
