# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_auto_20150409_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationwidget',
            name='urlconf_path',
            field=models.CharField(max_length=100, verbose_name='application'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='htmltextwidget',
            name='text',
            field=models.TextField(default=b'<p>Empty element</p>', verbose_name='text', blank=True),
            preserve_default=True,
        ),
    ]
