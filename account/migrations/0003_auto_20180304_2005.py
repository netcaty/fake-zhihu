# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20180225_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.CharField(max_length=10, choices=[(1, '男'), (0, '女')]),
        ),
    ]
