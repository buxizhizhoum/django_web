# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-05 03:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20170121_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='portrait',
            field=models.ImageField(blank=True, upload_to='/static/portrait'),
        ),
    ]
