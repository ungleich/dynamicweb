# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-04-24 04:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosting', '0027_auto_20160711_0210'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManageVMs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'managed': False,
            },
        ),
    ]
