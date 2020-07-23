# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-07-22 08:49
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zamrine_web_application', '0002_auto_20200722_0842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='currentPrice',
        ),
        migrations.RemoveField(
            model_name='product',
            name='longName',
        ),
        migrations.RemoveField(
            model_name='product',
            name='previousPrice',
        ),
        migrations.RemoveField(
            model_name='product',
            name='type',
        ),
        migrations.AddField(
            model_name='product',
            name='current_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='images',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), null=True, size=None),
        ),
        migrations.AddField(
            model_name='product',
            name='long_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='previous_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='related_products',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), null=True, size=None),
        ),
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=5), null=True, size=None),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='soldBy',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
