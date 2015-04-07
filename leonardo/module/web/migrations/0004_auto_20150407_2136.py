# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20150407_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='htmltextwidget',
            name='text',
            field=models.TextField(default=b'<p><django.utils.functional.__proxy__ object at 0x7f86185b5c50></p>', verbose_name='text', blank=True),
            preserve_default=True,
        ),
    ]
