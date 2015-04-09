# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import feincms.extensions


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewsEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('published', models.BooleanField(default=False, verbose_name='published')),
                ('title', models.CharField(help_text='This is used for the generated navigation too.', max_length=100, verbose_name='title')),
                ('slug', models.SlugField()),
                ('published_on', models.DateTimeField(help_text='Will be set automatically once you tick the `published` checkbox above.', null=True, verbose_name='published on', blank=True)),
            ],
            options={
                'ordering': ['-published_on'],
                'get_latest_by': 'published_on',
                'verbose_name': 'news entry',
                'verbose_name_plural': 'news entries',
            },
            bases=(models.Model, feincms.extensions.ExtensionsMixin),
        ),
    ]
