# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-17 15:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0002_userprofile_businessname'),
    ]

    operations = [
        migrations.AddField(
            model_name='photographer',
            name='image_1_desc',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='photographer',
            name='image_2_desc',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='photographer',
            name='image_3_desc',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='photographer',
            name='image_4_desc',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='photographer',
            name='image_5_desc',
            field=models.TextField(blank=True, null=True),
        ),
    ]
