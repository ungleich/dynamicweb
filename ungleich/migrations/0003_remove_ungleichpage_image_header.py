# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ungleich', '0002_ungleichpage_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ungleichpage',
            name='image_header',
        ),
    ]
