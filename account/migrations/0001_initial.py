# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('photo', models.ImageField(blank=True, upload_to='users')),
                ('sex', models.CharField(max_length=10, choices=[('m', '男'), ('f', '女')])),
                ('introduction', models.CharField(max_length=20, blank=True)),
                ('address', models.CharField(max_length=20, blank=True)),
                ('industry', models.CharField(max_length=20, blank=True)),
                ('education', models.CharField(max_length=20, blank=True)),
                ('website', models.URLField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
