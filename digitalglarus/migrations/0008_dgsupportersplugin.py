# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_auto_20150607_2207'),
        ('digitalglarus', '0007_auto_20160208_1031'),
    ]

    operations = [
        migrations.CreateModel(
            name='DGSupportersPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(primary_key=True, auto_created=True, parent_link=True, to='cms.CMSPlugin', serialize=False)),
                ('dgSupporters', models.ManyToManyField(to='digitalglarus.Supporter')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
