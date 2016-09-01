from autoslug import AutoSlugField
from django.db import models


class Base(models.Model):
    """Base class for Bucketlist and Item models to inherit from"""
    title = models.CharField(blank=False, max_length=200)
    description = models.TextField(blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class Bucketlist(Base):
    """ Creates bucketlist  """

    created_by = models.ForeignKey("auth.User",
                                   related_name="bucketlists",
                                   blank=True)
    slug = AutoSlugField(blank=False, populate_from='title', unique=True)
    image = models.ImageField(blank=True, null=True,
                              upload_to='bucketlist-images',
                              verbose_name="Bucket List Image")

    def __unicode__(self):
        return "{}: {}".format(self.id, self.title)


class Item(Base):
    """ Creates bucketlist item """

    item_bucketlist = models.ForeignKey("Bucketlist",
                                        related_name="items",
                                        blank=True)
    is_done = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title
