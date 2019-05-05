# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_emailactivation'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',

            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
