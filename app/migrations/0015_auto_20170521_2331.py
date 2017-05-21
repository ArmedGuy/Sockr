# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-21 21:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20170312_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Problem'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='runner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='app.Runner'),
        ),
    ]
