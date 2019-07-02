# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from book.constants import *

from users.models import *
from django.core.urlresolvers import reverse

# Create your models here.


def get_topic_image_path(instance, filename):
    """
    Function to return the image path for user images.

    Input Params:
        instance (obj): instance object
        filename (str): Original file name of the file
    Output Params:
        path (str): path name for the file
    """
    name = 'pics/%s/%s' % (
        instance.name,
        filename)
    return name


class Course(models.Model):
    name = models.CharField(
        default='', max_length=500, blank=True)
    description = models.CharField(
        default='', max_length=500, blank=True)
    image = models.ImageField(
        upload_to=get_topic_image_path,
        null=True, default=None, blank=True)


class Topic(models.Model):
    course = models.ForeignKey(Course)
    name = models.CharField(
        default='', max_length=500, blank=True)
    description = models.CharField(
        default='', max_length=500, blank=True)
    position = models.IntegerField()
    image = models.ImageField(
        upload_to=get_topic_image_path,
        null=True, default=None, blank=True)
    lock = models.BooleanField(default=True)

    def __unicode__(self):
        """Object name in django admin."""
        return '%s : %s' % (self.name, self.id)


class Content(models.Model):
    topic = models.ForeignKey(Topic)
    content = models.CharField(
        max_length=20, default=TEXT)
    position = models.IntegerField()
    value = models.TextField()

    def get_absolute_url(self):
        return reverse('content', kwargs={'pk': self.id})
    
    def __unicode__(self):
        """Object name in django admin."""
        return '%s : %s' % (self.position, self.topic.name)


class Completion(models.Model):
    user = models.ForeignKey(CustomUser)
    course = models.ForeignKey(Course)
    percent = models.FloatField(default=0.0)
    score = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def __unicode__(self):
        """Object name in django admin."""
        return '%s : %s' % (self.user.user.username, self.id)


class TopicCompletion(models.Model):
    completion = models.ForeignKey(Completion)
    topic = models.ForeignKey(Topic)
    complete = models.BooleanField(default=False)

class Suppliment(models.Model):
    topic = models.ForeignKey(Topic)
    description = models.TextField()
    sent = models.BooleanField(default=True)

    def __unicode__(self):
        """Object name in django admin."""
        return '%s : %s' % (self.topic.name, self.id)

