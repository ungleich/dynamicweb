# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('ungleich', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ungleichpage',
            name='image',
            field=filer.fields.image.FilerImageField(null=True, related_name='ungleinch_page_image', to='filer.Image', blank=True),
            preserve_default=True,
        ),
    ]
