# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-18 10:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0002_auto_20160818_1850'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterField(
            model_name='player',
            name='email',
            field=models.EmailField(max_length=255, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(blank=True, max_length=30, verbose_name='name'),
        ),
    ]