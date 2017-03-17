# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-12 12:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_runner'),
    ]

    operations = [
        migrations.AddField(
            model_name='runner',
            name='problems',
            field=models.ManyToManyField(related_name='problems', to='app.Problem'),
        ),
        migrations.AddField(
            model_name='submission',
            name='runner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.Runner'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='runner',
            name='secret_key',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]