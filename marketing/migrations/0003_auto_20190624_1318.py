# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-06-24 13:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0002_marketingpreference_mailchimp_subscribed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketingpreference',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='marketing', to=settings.AUTH_USER_MODEL),
        ),
    ]
