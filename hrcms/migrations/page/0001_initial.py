# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import feincms.module.extensions.datepublisher
import feincms.module.mixins
import feincms.extensions


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
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
                ('publication_date', models.DateTimeField(default=feincms.module.extensions.datepublisher.granular_now, verbose_name='publication date')),
                ('publication_end_date', models.DateTimeField(help_text='Leave empty if the entry should stay active forever.', null=True, verbose_name='publication end date', blank=True)),
                ('language', models.CharField(default=b'cs', max_length=10, verbose_name='language', choices=[(b'cs', b'CS'), (b'en', b'EN')])),
                ('navigation_extension', models.CharField(help_text='Select the module providing subpages for this page if you need to customize the navigation.', max_length=200, null=True, verbose_name='navigation extension', blank=True)),
                ('_content_title', models.TextField(help_text='The first line is the main title, the following lines are subtitles.', verbose_name='content title', blank=True)),
                ('_page_title', models.CharField(help_text='Page title for browser window. Same as title bydefault. Must not be longer than 70 characters.', max_length=69, verbose_name='page title', blank=True)),
                ('navigation_group', models.CharField(default='default', max_length=20, verbose_name='navigation group', db_index=True, choices=[('default', 'Default'), ('footer', 'Footer')])),
                ('meta_keywords', models.TextField(help_text='Keywords are ignored by most search engines.', verbose_name='meta keywords', blank=True)),
                ('meta_description', models.TextField(help_text='This text is displayed on the search results page. It is however not used for the SEO ranking. Text longer than 140 characters is truncated.', verbose_name='meta description', blank=True)),
                ('featured', models.BooleanField(verbose_name='featured')),
                ('excerpt', models.TextField(help_text='Add a brief excerpt summarizing the content of this page.', verbose_name='excerpt', blank=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', null=True, editable=False)),
                ('modification_date', models.DateTimeField(verbose_name='modification date', null=True, editable=False)),
                ('template_key', models.CharField(default=b'base.html', max_length=255, verbose_name='template', choices=[(b'base.html', 'Standard template')])),
                ('parent', models.ForeignKey(related_name='children', verbose_name='Parent', blank=True, to='page.Page', null=True)),
                ('related_pages', models.ManyToManyField(help_text='Select pages that should be listed as related content.', related_name='page_page_related', null=True, to='page.Page', blank=True)),
                ('symlinked_page', models.ForeignKey(related_name='page_page_symlinks', blank=True, to='page.Page', help_text='All content is inherited from this page if given.', null=True, verbose_name='symlinked page')),
                ('translation_of', models.ForeignKey(related_name='translations', blank=True, to='page.Page', help_text='Leave this empty for entries in the primary language.', null=True, verbose_name='translation of')),
            ],
            options={
                'ordering': ['tree_id', 'lft'],
                'verbose_name': 'page',
                'verbose_name_plural': 'pages',
            },
            bases=(models.Model, feincms.extensions.ExtensionsMixin, feincms.module.mixins.ContentModelMixin),
        ),
    ]
