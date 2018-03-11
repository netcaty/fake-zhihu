# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.CharField(max_length=10, default='m', choices=[('m', '男'), ('f', '女')]),
        ),
    ]
