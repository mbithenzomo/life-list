# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-21 15:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_bucketlist_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bucketlist',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=b'lifelist/api/static/bucketlist-images', verbose_name=b'Bucket List Image'),
        ),
    ]