# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-18 12:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_chatcontent_create_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(blank=True, null=True, to='blog.User'),
        ),
    ]
