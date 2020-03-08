# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2020-02-18 19:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0016_auto_20200218_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='billing_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card', to='billing.BillingProfile'),
        ),
    ]