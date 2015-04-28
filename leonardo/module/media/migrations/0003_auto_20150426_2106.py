# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '__first__'),
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
    ]
