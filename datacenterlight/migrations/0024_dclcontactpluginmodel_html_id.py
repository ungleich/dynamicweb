# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2018-05-25 13:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenterlight', '0023_auto_20180524_0349'),
    ]

    operations = [
        migrations.AddField(
            model_name='dclcontactpluginmodel',
            name='html_id',
            field=models.SlugField(blank=True, help_text='An optional html id for the Conatct Section. Required to set as target of any link.', null=True),
        ),
    ]
