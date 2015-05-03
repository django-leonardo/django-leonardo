# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import leonardo.module.media.models


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '__first__'),
        ('media', '0003_auto_20150426_2106'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flash',
            fields=[
                ('file_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='filer.File')),
            ],
            options={
                'verbose_name': 'flash video',
                'verbose_name_plural': 'flash videos',
            },
            bases=(leonardo.module.media.models.MediaMixin, 'filer.file'),
        ),
    ]
