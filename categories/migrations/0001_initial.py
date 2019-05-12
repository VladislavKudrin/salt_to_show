# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-05-08 16:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accessories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('belts', models.CharField(max_length=120)),
                ('hats', models.CharField(max_length=120)),
                ('wallets', models.CharField(max_length=120)),
                ('other', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Bottoms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pants', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accessories', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='categories.Accessories')),
                ('bottoms', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='categories.Bottoms')),
            ],
        ),
        migrations.CreateModel(
            name='Footwear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sneakers', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Outwear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heavy_coats', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Tops',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shirt', models.CharField(max_length=120)),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='footwear',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='categories.Footwear'),
        ),
        migrations.AddField(
            model_name='category',
            name='outwear',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='categories.Outwear'),
        ),
        migrations.AddField(
            model_name='category',
            name='tops',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='categories.Tops'),
        ),
    ]
