# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-30 03:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swot', '0006_auto_20180226_0404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='item',
        ),
        migrations.DeleteModel(
            name='Vote',
        ),
    ]
