# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-04 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FirstProjectRefactor', '0013_post_nr_of_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='nr_of_likes',
            field=models.IntegerField(default=0),
        ),
    ]
