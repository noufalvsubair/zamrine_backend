# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-07-22 22:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zamrine_web_application', '0022_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='short_name',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
