# coding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserType(models.Model):
    user_type = models.CharField(max_length=100, default="Guest")

    def __unicode__(self):
        return self.user_type

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    portrait = models.ImageField(upload_to="portrait/", blank=True)
    friends = models.ManyToManyField("User",blank=True)
    user_type = models.ForeignKey("UserType")

    def __unicode__(self):
        return self.username

class Notes(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    favor_count = models.IntegerField(default=0)
    reply_count = models.IntegerField(default=0)
    username = models.ForeignKey("User")
    notes_type = models.ForeignKey("NotesType")

    def __unicode__(self):
        return self.title

class Reply(models.Model):
    content = models.CharField(max_length=1000)
    user = models.ForeignKey("User")
    notes = models.ForeignKey("Notes", default=0)

    def __unicode__(self):
        return self.content

class NotesType(models.Model):
    notes_type = models.CharField(max_length=100)

    def __unicode__(self):
        return self.notes_type

class ChatContent(models.Model):

    content = models.CharField(max_length=300)
    user = models.ForeignKey("User")
    create_date = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def __unicode__(self):
        return self.content