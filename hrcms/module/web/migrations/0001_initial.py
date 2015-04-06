# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import feincms.module.extensions.datepublisher
import feincms.contrib.fields
import feincms.extensions
import feincms.contrib.richtext
import feincms.module.mixins


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parameters', feincms.contrib.fields.JSONField(null=True, editable=False)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('urlconf_path', models.CharField(max_length=100, verbose_name='application', choices=[(b'hrcms.portal.device_catalog.urls', b'Robotice Device Catalog'), (b'elephantblog.urls', b'Blog'), (b'hrcms.module.eshop.urls', b'Eshop'), (b'hrcms.module.eshop.api.urls', b'Eshop API'), (b'hrcms.module.auth.urls', b'API Auth')])),
            ],
            options={
                'ordering': ['ordering'],
                'abstract': False,
                'verbose_name_plural': 'application contents',
                'db_table': 'web_page_applicationcontent',
                'verbose_name': 'application content',
                'permissions': [],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('title', models.CharField(help_text='This title is also used for navigation menu items.', max_length=200, verbose_name='title')),
                ('slug', models.SlugField(help_text='This is used to build the URL for this page', max_length=150, verbose_name='slug')),
                ('in_navigation', models.BooleanField(default=False, verbose_name='in navigation')),
                ('override_url', models.CharField(help_text="Override the target URL. Be sure to include slashes at the beginning and at the end if it is a local URL. This affects both the navigation and subpages' URLs.", max_length=255, verbose_name='override URL', blank=True)),
                ('redirect_to', models.CharField(help_text='Target URL for automatic redirects or the primary key of a page.', max_length=255, verbose_name='redirect to', blank=True)),
                ('_cached_url', models.CharField(default='', editable=False, max_length=255, blank=True, verbose_name='Cached URL', db_index=True)),
                ('col1_width', models.IntegerField(default=12, verbose_name='Column 1 width', choices=[(0, b' \xe2\x80\x94 '), (1, '1 col'), (2, '2 cols'), (3, '3 cols'), (4, '4 cols'), (5, '5 cols'), (6, '6 cols'), (7, '7 cols'), (8, '8 cols'), (9, '9 cols'), (10, '10 cols'), (11, '11 cols'), (12, '12 cols')])),
                ('col2_width', models.IntegerField(default=12, verbose_name='Column 2 width', choices=[(0, b' \xe2\x80\x94 '), (1, '1 col'), (2, '2 cols'), (3, '3 cols'), (4, '4 cols'), (5, '5 cols'), (6, '6 cols'), (7, '7 cols'), (8, '8 cols'), (9, '9 cols'), (10, '10 cols'), (11, '11 cols'), (12, '12 cols')])),
                ('col3_width', models.IntegerField(default=12, verbose_name='Column 3 width', choices=[(0, b' \xe2\x80\x94 '), (1, '1 col'), (2, '2 cols'), (3, '3 cols'), (4, '4 cols'), (5, '5 cols'), (6, '6 cols'), (7, '7 cols'), (8, '8 cols'), (9, '9 cols'), (10, '10 cols'), (11, '11 cols'), (12, '12 cols')])),
                ('col4_width', models.IntegerField(default=12, verbose_name='Column 4 width', choices=[(0, b' \xe2\x80\x94 '), (1, '1 col'), (2, '2 cols'), (3, '3 cols'), (4, '4 cols'), (5, '5 cols'), (6, '6 cols'), (7, '7 cols'), (8, '8 cols'), (9, '9 cols'), (10, '10 cols'), (11, '11 cols'), (12, '12 cols')])),
                ('template_name', models.CharField(help_text='Core HTML templates and CSS styles.', max_length=255, null=True, verbose_name=b'Template', blank=True)),
                ('theme', models.CharField(help_text='Color and style extension to the template.', max_length=255, null=True, verbose_name='Theme', blank=True)),
                ('template_key', models.CharField(default=b'layout_flex', max_length=255, verbose_name='template', choices=[(b'layout_flex', '1 column'), (b'layout_flex_flex', '2 same columns'), (b'layout_flex_fixed', '2 columns right'), (b'layout_fixed_flex', '2 columns left'), (b'layout_fixed_flex_fixed', '3 columns'), (b'layout_flex_flex_flex', '3 same columns'), (b'dashboard', 'Dashboard'), (b'api', 'API')])),
                ('publication_date', models.DateTimeField(default=feincms.module.extensions.datepublisher.granular_now, verbose_name='publication date')),
                ('publication_end_date', models.DateTimeField(help_text='Leave empty if the entry should stay active forever.', null=True, verbose_name='publication end date', blank=True)),
                ('language', models.CharField(default=b'cs', max_length=10, verbose_name='language', choices=[(b'cs', b'CS'), (b'en', b'EN')])),
                ('navigation_extension', models.CharField(help_text='Select the module providing subpages for this page if you need to customize the navigation.', max_length=200, null=True, verbose_name='navigation extension', blank=True)),
                ('meta_keywords', models.TextField(help_text='Keywords are ignored by most search engines.', verbose_name='meta keywords', blank=True)),
                ('meta_description', models.TextField(help_text='This text is displayed on the search results page. It is however not used for the SEO ranking. Text longer than 140 characters is truncated.', verbose_name='meta description', blank=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', null=True, editable=False)),
                ('modification_date', models.DateTimeField(verbose_name='modification date', null=True, editable=False)),
                ('parent', models.ForeignKey(related_name='children', verbose_name='Parent', blank=True, to='web.Page', null=True)),
                ('symlinked_page', models.ForeignKey(related_name='web_page_symlinks', blank=True, to='web.Page', help_text='All content is inherited from this page if given.', null=True, verbose_name='symlinked page')),
                ('translation_of', models.ForeignKey(related_name='translations', blank=True, to='web.Page', help_text='Leave this empty for entries in the primary language.', null=True, verbose_name='translation of')),
            ],
            options={
                'ordering': ['tree_id', 'lft'],
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
            },
            bases=(models.Model, feincms.extensions.ExtensionsMixin, feincms.module.mixins.ContentModelMixin),
        ),
        migrations.CreateModel(
            name='RichTextContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', feincms.contrib.richtext.RichTextField(verbose_name='text', blank=True)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('parent', models.ForeignKey(related_name='richtextcontent_set', to='web.Page')),
            ],
            options={
                'ordering': ['ordering'],
                'abstract': False,
                'verbose_name_plural': 'rich texts',
                'db_table': 'web_page_richtextcontent',
                'verbose_name': 'rich text',
                'permissions': [],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='applicationcontent',
            name='parent',
            field=models.ForeignKey(related_name='applicationcontent_set', to='web.Page'),
            preserve_default=True,
        ),
    ]
