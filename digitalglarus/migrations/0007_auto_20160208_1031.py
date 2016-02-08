# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digitalglarus', '0006_dggallery_dggalleryplugin_dgpicture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supporter',
            name='description',
            field=models.TextField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
