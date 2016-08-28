# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-16 09:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bucketlist',
            name='created_by',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='bucketlists', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bucketlist',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='bucketlist',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='bucketlist',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='api.Bucketlist'),
        ),
        migrations.AlterField(
            model_name='item',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]