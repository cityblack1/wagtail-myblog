# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-08-17 07:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='名字')),
                ('email', models.EmailField(max_length=100, verbose_name='邮箱')),
                ('url', models.CharField(max_length=100, verbose_name='网址')),
                ('comment', models.TextField(verbose_name='评论')),
                ('date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='发布日期')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.BlogPage', verbose_name='博文')),
            ],
        ),
    ]
