# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-08-07 17:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('analitics', '0002_usersession'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegionPreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(blank=True, max_length=120, null=True)),
                ('currency', models.CharField(blank=True, default='USD', max_length=120, null=True)),
                ('user', models.ManyToManyField(blank=True, related_name='region_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
