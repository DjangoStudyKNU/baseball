# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-07 14:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0002_auto_20160903_1557'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='amatuer_team',
            new_name='amateur_team',
        ),
    ]
