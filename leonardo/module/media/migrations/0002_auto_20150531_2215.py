# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import leonardo.module.media.fields.multistorage_file


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='folder',
            options={'ordering': ('name',), 'verbose_name': 'Folder', 'verbose_name_plural': 'Folders', 'permissions': (('can_use_folder_listing', 'Can use Folder listing'),)},
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=leonardo.module.media.fields.multistorage_file.MultiStorageFileField(max_length=255, upload_to=leonardo.module.media.fields.multistorage_file.generate_filename_multistorage, null=True, verbose_name='file', blank=True),
            preserve_default=True,
        ),
    ]
