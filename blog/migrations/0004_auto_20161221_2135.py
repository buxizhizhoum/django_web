# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-21 13:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20161217_2352'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=300)),
                ('uer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.User')),
            ],
        ),
        migrations.AlterField(
            model_name='usertype',
            name='user_type',
            field=models.CharField(default='Guest', max_length=100),
        ),
    ]
