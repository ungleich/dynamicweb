# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digitalglarus', '0008_dgsupportersplugin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dgsupportersplugin',
            name='dgSupporters',
        ),
    ]
