# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-22 15:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xapp', '0014_auto_20180521_1826'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='bookings',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='tripmaker',
        ),
        migrations.DeleteModel(
            name='Trip',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
