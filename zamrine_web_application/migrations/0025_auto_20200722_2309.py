# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-07-22 23:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zamrine_web_application', '0024_auto_20200722_2209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='user',
        ),
        migrations.DeleteModel(
            name='Person',
        ),
    ]
