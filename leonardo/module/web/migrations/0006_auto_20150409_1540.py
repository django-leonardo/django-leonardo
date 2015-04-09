# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20150409_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationwidget',
            name='template_name',
            field=models.CharField(default=b'default', max_length=255, verbose_name='Display'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='breadcrumbswidget',
            name='template_name',
            field=models.CharField(default=b'default', max_length=255, verbose_name='Display'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contentnavigationwidget',
            name='template_name',
            field=models.CharField(default=b'default', max_length=255, verbose_name='Display'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contextnavigationwidget',
            name='template_name',
            field=models.CharField(default=b'default', max_length=255, verbose_name='Display'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='feedreaderwidget',
            name='template_name',
            field=models.CharField(default=b'default', max_length=255, verbose_name='Display'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='formwidget',
            name='template_name',
            field=models.CharField(default=b'default', max_length=255, verbose_name='Display'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='htmltextwidget',
            name='template_name',
            field=models.CharField(default=b'default', max_length=255, verbose_name='Display'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='languageselectorwidget',
            name='template_name',
            field=models.CharField(default=b'default', max_length=255, verbose_name='Display'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='linearnavigationwidget',
            name='template_name',
            field=models.CharField(default=b'default', max_length=255, verbose_name='Display'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='markuptextwidget',
            name='template_name',
            field=models.CharField(default=b'default', max_length=255, verbose_name='Display'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='siteheadingwidget',
            name='template_name',
            field=models.CharField(default=b'default', max_length=255, verbose_name='Display'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sitemapwidget',
            name='template_name',
            field=models.CharField(default=b'default', max_length=255, verbose_name='Display'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sitesearchwidget',
            name='template_name',
            field=models.CharField(default=b'default', max_length=255, verbose_name='Display'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='treenavigationwidget',
            name='template_name',
            field=models.CharField(default=b'default', max_length=255, verbose_name='Display'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='htmltextwidget',
            name='text',
            field=models.TextField(default=b'<p><django.utils.functional.__proxy__ object at 0x7f3ac0833110></p>', verbose_name='text', blank=True),
            preserve_default=True,
        ),
    ]
