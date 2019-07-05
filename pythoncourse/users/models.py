"""Models of app users."""
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse
SupplierMailToken = 0


def get_user_image_path(instance, filename):
    """
    Function to return the image path for user images.

    Input Params:
        instance (obj): instance object
        filename (str): Original file name of the file
    Output Params:
        path (str): path name for the file
    """
    name = 'profilepic/%s/%s/%s' % (
        instance.user_type,
        instance.user.first_name, filename)
    return name


class CustomUser(models.Model):
    """
    Root User model.

    Atribs:
        user (obj): Django user model.
        type (int): field define the type of the user like
            admin or CB etc.
        access_token (char): Hex value representing the token of the
            user.
        image (img): user image.
        address(char): address of the user.
        active_devices (int): no of active devices of user.
        blocked(bool): field which shows the active status of user.
        phone (char): phone number of the user
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.IntegerField(default=4)
    level = models.IntegerField(default=0)
    access_token = models.CharField(default='', max_length=100)
    description = models.CharField(
        default='', max_length=2000, blank=True)
    phone = models.CharField(
        default='', max_length=200, blank=True)
    image = models.ImageField(
        upload_to=get_user_image_path,
        null=True, default=None, blank=True)
    blocked = models.BooleanField(default=False)


    @property
    def name(self):
        """Get user name."""
        return self.user.get_full_name()

    @property
    def image_url(self):
        """Get file url name."""
        try:
            return self.image.url
        except:
            None

    def __unicode__(self):
        """Object name in django admin."""
        return '%s : %s' % (self.name, self.id)


class PasswordSetter(models.Model):
    """
    Class to store the password set data.

    Atribs:
        user(obj): user object
        access_token (str): token to reset password.
        type(int): type indicating the event associated.
        expires_at(datetime): time up to which link is valid.
        browser(char): browser of the user requested.
        location(char): location of the request created.
    """

    user = models.ForeignKey(CustomUser)
    type = models.IntegerField(default=1)
    browser = models.CharField(
        default='', max_length=500, blank=True)
    location = models.CharField(
        default='', max_length=500, blank=True)
    reset_token = models.CharField(
        default='', max_length=200, blank=True)
    expires_at = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        """Object name in django admin."""
        return '%s%s' % (self.user.name, self.id)


class Admin(models.Model):
    """
    Class representing admin.

    Atribs:
        user(obj): user object
    """

    user = models.OneToOneField(CustomUser)

    @property
    def name(self):
        """Get user name."""
        return self.user.name

    def __unicode__(self):
        """Object name in django admin."""
        return '%s : %s' % (self.name, self.id)
