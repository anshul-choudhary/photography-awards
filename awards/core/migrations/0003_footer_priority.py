# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-07 14:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20160407_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='footer',
            name='priority',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Order in which it will appear'),
        ),
    ]