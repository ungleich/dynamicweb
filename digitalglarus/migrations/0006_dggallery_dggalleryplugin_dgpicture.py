# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_auto_20150607_2207'),
        ('filer', '0002_auto_20160208_0200'),
        ('digitalglarus', '0005_auto_20160208_0218'),
    ]

    operations = [
        migrations.CreateModel(
            name='DGGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('parent', models.ForeignKey(blank=True, to='digitalglarus.DGGallery', null=True)),
            ],
            options={
                'verbose_name_plural': 'dgGallery',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DGGalleryPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(primary_key=True, to='cms.CMSPlugin', auto_created=True, parent_link=True, serialize=False)),
                ('dgGallery', models.ForeignKey(to='digitalglarus.DGGallery')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='DGPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('description', models.CharField(max_length=60)),
                ('gallery', models.ForeignKey(to='digitalglarus.DGGallery')),
                ('image', filer.fields.image.FilerImageField(related_name='dg_gallery', to='filer.Image')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
