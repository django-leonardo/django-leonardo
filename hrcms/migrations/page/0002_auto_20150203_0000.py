# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import feincms.module.medialibrary.fields
import feincms.contrib.richtext


class Migration(migrations.Migration):

    dependencies = [
        ('medialibrary', '__first__'),
        ('page', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaFileContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('type', models.CharField(default=b'default', max_length=20, verbose_name='type', choices=[(b'default', 'default'), (b'lightbox', 'lightbox')])),
                ('mediafile', feincms.module.medialibrary.fields.MediaFileForeignKey(related_name='+', verbose_name='media file', to='medialibrary.MediaFile')),
                ('parent', models.ForeignKey(related_name='mediafilecontent_set', to='page.Page')),
            ],
            options={
                'ordering': ['ordering'],
                'abstract': False,
                'verbose_name_plural': 'media files',
                'db_table': 'page_page_mediafilecontent',
                'verbose_name': 'media file',
                'permissions': [],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RichTextContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', feincms.contrib.richtext.RichTextField(verbose_name='text', blank=True)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('parent', models.ForeignKey(related_name='richtextcontent_set', to='page.Page')),
            ],
            options={
                'ordering': ['ordering'],
                'abstract': False,
                'verbose_name_plural': 'rich texts',
                'db_table': 'page_page_richtextcontent',
                'verbose_name': 'rich text',
                'permissions': [],
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='page',
            name='navigation_extension',
            field=models.CharField(choices=[('hrcms.portal.models.PortalExtension', b'portal')], max_length=200, blank=True, help_text='Select the module providing subpages for this page if you need to customize the navigation.', null=True, verbose_name='navigation extension'),
        ),
    ]
