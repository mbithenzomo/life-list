# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-21 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20160816_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='bucketlist',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=b'bucketlists', verbose_name=b'Bucket List Image'),
        ),
    ]
