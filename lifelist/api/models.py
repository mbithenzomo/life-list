from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Bucketlist(models.Model):
    """ Creates bucketlist  """

    created_by = models.ForeignKey("auth.User")
    title = models.CharField
    description = models.TextField
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(default=timezone.now)

    def __repr__(self):
        return "<Bucketlist: %r>" % self.title


class Item(models.Model):
    """ Creates items item """

    created_by = models.ForeignKey("auth.User")
    bucketlist = models.ForeignKey("Bucketlist")
    title = models.CharField
    description = models.TextField
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(default=timezone.now)
    is_done = models.BooleanField(default=False)

    def __repr__(self):
        return "<Bucketlist Item: %r>" % self.title
