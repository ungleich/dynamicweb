# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-07 20:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0006_auto_20160526_0445'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_superuser',
        ),
    ]
