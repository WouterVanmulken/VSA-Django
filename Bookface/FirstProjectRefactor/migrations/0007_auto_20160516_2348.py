# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-16 21:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('FirstProjectRefactor', '0006_auto_20160516_2344'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Employee',
            new_name='UserInfo',
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 16, 21, 47, 17, 549467, tzinfo=utc), verbose_name='date published'),
        ),
    ]
