# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-20 08:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0005_auto_20160820_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='rate',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=20, null=True),
        ),
    ]
