# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2020-03-05 15:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0022_feedback'),
        ('orders', '0020_auto_20200214_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='feedback',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='billing.Feedback'),
        ),
    ]
