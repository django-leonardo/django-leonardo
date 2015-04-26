# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '__first__'),
        ('web', '0004_auto_20150426_1515'),
        ('media', '0002_leonardofile_leonardofolder'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vector',
            fields=[
                ('file_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='filer.File')),
            ],
            options={
                'verbose_name': 'vector',
                'verbose_name_plural': 'vetors',
            },
            bases=('filer.file',),
        ),
        migrations.RemoveField(
            model_name='leonardofile',
            name='file_ptr',
        ),
        migrations.DeleteModel(
            name='LeonardoFile',
        ),
    ]
