# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-31 11:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20161231_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='error',
            name='key',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='problem',
            name='test_key',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
    ]
