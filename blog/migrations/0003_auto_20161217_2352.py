# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-17 15:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20161216_2231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notes',
            name='reply',
        ),
        migrations.AddField(
            model_name='reply',
            name='notes',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='blog.Notes'),
        ),
    ]
