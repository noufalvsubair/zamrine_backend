# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-07-22 09:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zamrine_web_application', '0008_auto_20200722_0935'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductSizes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'ExtraLarge')], max_length=2)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='images',
        ),
        migrations.RemoveField(
            model_name='product',
            name='related_products',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sizes',
        ),
        migrations.AddField(
            model_name='productsizes',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zamrine_web_application.Product'),
        ),
        migrations.AddField(
            model_name='productimages',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zamrine_web_application.Product'),
        ),
    ]
