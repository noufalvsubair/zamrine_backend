# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-07-22 09:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zamrine_web_application', '0009_auto_20200722_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimages',
            name='image_url',
            field=models.URLField(null=True),
        ),
    ]
