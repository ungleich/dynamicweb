# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0003_auto_20160306_2306'),
        ('cms', '0013_urlconfrevision'),
    ]

    operations = [
        migrations.CreateModel(
            name='DGGallery',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=30)),
                ('parent', models.ForeignKey(null=True, to='digitalglarus.DGGallery', blank=True)),
            ],
            options={
                'verbose_name_plural': 'dgGallery',
            },
        ),
        migrations.CreateModel(
            name='DGGalleryPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(primary_key=True, serialize=False, to='cms.CMSPlugin', auto_created=True, parent_link=True)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('description', models.CharField(max_length=60)),
                ('gallery', models.ForeignKey(to='digitalglarus.DGGallery')),
                ('image', filer.fields.image.FilerImageField(related_name='dg_gallery', to='filer.Image')),
            ],
        ),
        migrations.CreateModel(
            name='DGSupportersPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(primary_key=True, serialize=False, to='cms.CMSPlugin', auto_created=True, parent_link=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('received_date', models.DateTimeField(verbose_name='date received')),
            ],
        ),
        migrations.CreateModel(
            name='Supporter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(null=True, blank=True)),
            ],
        ),
    ]
