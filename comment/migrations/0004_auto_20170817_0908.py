# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-08-17 09:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_auto_20170817_0905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='url',
            field=models.CharField(blank=True, max_length=100, verbose_name='网址'),
        ),
    ]
