# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-16 11:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('content', models.TextField()),
                ('favor_count', models.IntegerField(default=0)),
                ('reply_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='NotesType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes_type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1000)),
                ('notes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Notes')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.UserType'),
        ),
        migrations.AddField(
            model_name='reply',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.User'),
        ),
        migrations.AddField(
            model_name='notes',
            name='notes_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.NotesType'),
        ),
        migrations.AddField(
            model_name='notes',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.User'),
        ),
    ]
