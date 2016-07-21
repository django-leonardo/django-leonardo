# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0003_auto_20150723_1313'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vector',
            options={'verbose_name': 'vector', 'verbose_name_plural': 'vectors'},
        ),
    ]
