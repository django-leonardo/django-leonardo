# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('file_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='filer.File')),
            ],
            options={
                'verbose_name': 'document',
                'verbose_name_plural': 'documents',
            },
            bases=('filer.file',),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('file_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='filer.File')),
                ('_height', models.IntegerField(null=True, blank=True)),
                ('_width', models.IntegerField(null=True, blank=True)),
                ('default_alt_text', models.CharField(max_length=255, null=True, verbose_name='default alt text', blank=True)),
                ('default_caption', models.CharField(max_length=255, null=True, verbose_name='default caption', blank=True)),
                ('subject_location', models.CharField(default=None, max_length=64, null=True, verbose_name='subject location', blank=True)),
                ('date_taken', models.DateTimeField(verbose_name='date taken', null=True, editable=False, blank=True)),
                ('author', models.CharField(max_length=255, null=True, verbose_name='author', blank=True)),
                ('must_always_publish_author_credit', models.BooleanField(default=False, verbose_name='must always publish author credit')),
                ('must_always_publish_copyright', models.BooleanField(default=False, verbose_name='must always publish copyright')),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
            bases=('filer.file',),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('file_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='filer.File')),
            ],
            options={
                'verbose_name': 'video',
                'verbose_name_plural': 'videos',
            },
            bases=('filer.file',),
        ),
    ]
