# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_question_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='tags',
            new_name='topics',
        ),
    ]
