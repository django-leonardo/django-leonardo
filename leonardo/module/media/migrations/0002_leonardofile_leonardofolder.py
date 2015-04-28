# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '__first__'),
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeonardoFolder',
            fields=[
                ('folder_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='filer.Folder')),
            ],
            options={
                'verbose_name': 'folder',
                'verbose_name_plural': 'folders',
            },
            bases=('filer.folder',),
        ),
    ]
