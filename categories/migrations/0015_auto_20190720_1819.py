# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-07-20 18:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0014_remove_overcategory_overcategory_for'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_for',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.Gender'),
        ),
        migrations.AlterField(
            model_name='gender',
            name='gender_for',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.Overcategory'),
        ),
        migrations.AlterField(
            model_name='undercategory',
            name='undercategory_for',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.Category'),
        ),
    ]
