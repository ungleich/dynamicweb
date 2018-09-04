# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-09-04 21:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('digitalglarus', '0028_auto_20180904_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dggalleryplugin',
            name='cmsplugin_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='digitalglarus_dggalleryplugin', serialize=False, to='cms.CMSPlugin'),
        ),
        migrations.AlterField(
            model_name='dgsupportersplugin',
            name='cmsplugin_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='digitalglarus_dgsupportersplugin', serialize=False, to='cms.CMSPlugin'),
        ),
    ]
