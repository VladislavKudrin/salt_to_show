# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-06-15 05:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat_ecommerce', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_read', models.BooleanField(default=False)),
                ('notification_chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat_ecommerce.ChatMessage')),
                ('notification_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
