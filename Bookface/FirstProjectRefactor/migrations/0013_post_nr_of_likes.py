# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-04 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FirstProjectRefactor', '0012_auto_20160526_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='nr_of_likes',
            field=models.IntegerField(default=0, max_length=100),
        ),
    ]
