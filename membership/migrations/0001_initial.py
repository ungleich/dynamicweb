# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('validated', models.IntegerField(default=0, choices=[(0, 'Not validated'), (1, 'Validated')])),
                ('validation_slug', models.CharField(unique=True, max_length=50, db_index=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CreditCards',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('card_number', models.CharField(max_length=50)),
                ('expiry_date', models.CharField(validators=[django.core.validators.RegexValidator('\\d{2}\\/\\d{4}', 'Use this pattern(MM/YYYY).')], max_length=50)),
                ('ccv', models.CharField(validators=[django.core.validators.RegexValidator('\\d{3,4}', 'Wrong CCV number.')], max_length=4)),
                ('payment_type', models.CharField(max_length=5, default='N')),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
