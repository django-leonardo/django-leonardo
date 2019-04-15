# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0004_auto_20160711_0759'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='ordering',
            field=models.IntegerField(null=True, verbose_name='ordering', blank=True),
        ),
        migrations.AddField(
            model_name='folder',
            name='ordering',
            field=models.IntegerField(null=True, verbose_name='ordering', blank=True),
        ),
        migrations.AlterField(
            model_name='documenttranslation',
            name='language_code',
            field=models.CharField(default=b'en', verbose_name='language', max_length=10, editable=False, choices=[[b'en', b'EN']]),
        ),
        migrations.AlterField(
            model_name='foldertranslation',
            name='language_code',
            field=models.CharField(default=b'en', verbose_name='language', max_length=10, editable=False, choices=[[b'en', b'EN']]),
        ),
        migrations.AlterField(
            model_name='imagetranslation',
            name='language_code',
            field=models.CharField(default=b'en', verbose_name='language', max_length=10, editable=False, choices=[[b'en', b'EN']]),
        ),
        migrations.AlterField(
            model_name='vectortranslation',
            name='language_code',
            field=models.CharField(default=b'en', verbose_name='language', max_length=10, editable=False, choices=[[b'en', b'EN']]),
        ),
        migrations.AlterField(
            model_name='videotranslation',
            name='language_code',
            field=models.CharField(default=b'en', verbose_name='language', max_length=10, editable=False, choices=[[b'en', b'EN']]),
        ),
    ]
