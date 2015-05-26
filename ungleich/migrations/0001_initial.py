# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0011_auto_20150419_1006'),
    ]

    operations = [
        migrations.CreateModel(
            name='UngleichPage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('image_header', models.ImageField(upload_to='image_header')),
                ('extended_object', models.OneToOneField(editable=False, to='cms.Page')),
                ('public_extension', models.OneToOneField(editable=False, related_name='draft_extension', null=True, to='ungleich.UngleichPage')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
