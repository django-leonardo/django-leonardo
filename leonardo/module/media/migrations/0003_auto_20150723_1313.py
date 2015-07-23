# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0002_auto_20150531_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clipboard',
            name='user',
            field=models.ForeignKey(related_name='media_clipboards', verbose_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
