# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-19 15:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0002_auto_20160518_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='end_date',
            field=models.DateTimeField(null=True, verbose_name='date finished'),
        ),
        migrations.AlterField(
            model_name='work',
            name='end_time',
            field=models.DateTimeField(null=True, verbose_name='date finished'),
        ),
    ]
