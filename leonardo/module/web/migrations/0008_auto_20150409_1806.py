# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import feincms.extensions
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_auto_20150409_1544'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogCategoriesWidget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('options', django_extensions.db.fields.json.JSONField(verbose_name='widget options', editable=False, blank=True)),
                ('prerendered_content', models.TextField(verbose_name='prerendered content', editable=False, blank=True)),
                ('label', models.CharField(max_length=255, null=True, verbose_name='Title', blank=True)),
                ('template_name', models.CharField(default=b'default.html', max_length=255, verbose_name='Display')),
                ('span', models.IntegerField(default=12, verbose_name='Span', choices=[(0, b' \xe2\x80\x94 '), (1, '1 col'), (2, '2 cols'), (3, '3 cols'), (4, '4 cols'), (5, '5 cols'), (6, '6 cols'), (7, '7 cols'), (8, '8 cols'), (9, '9 cols'), (10, '10 cols'), (11, '11 cols'), (12, '12 cols')])),
                ('vertical_span', models.IntegerField(default=12, verbose_name='V. Span', choices=[(0, b' \xe2\x80\x94 '), (1, '1 row'), (2, '2 rows'), (3, '3 rows'), (4, '4 rows'), (5, '5 rows'), (6, '6 rows'), (7, '7 rows'), (8, '8 rows'), (9, '9 rows'), (10, '10 rows'), (11, '11 rows'), (12, '12 rows'), (13, '13 rows'), (14, '14 rows'), (15, '15 rows'), (16, '16 rows'), (17, '17 rows'), (18, '18 rows'), (19, '19 rows'), (20, '20 rows'), (21, '21 rows'), (22, '22 rows'), (23, '23 rows'), (24, '24 rows')])),
                ('align', models.IntegerField(default=0, verbose_name='Alignment', choices=[(0, 'auto'), (1, 'left'), (2, 'center'), (3, 'right')])),
                ('vertical_align', models.IntegerField(default=0, verbose_name='V. Alignment', choices=[(0, 'auto'), (1, 'top'), (2, 'middle'), (3, 'bottom')])),
                ('prepend', models.IntegerField(default=12, verbose_name='Prepend', choices=[(0, b' \xe2\x80\x94 '), (1, '1 col'), (2, '2 cols'), (3, '3 cols'), (4, '4 cols'), (5, '5 cols'), (6, '6 cols'), (7, '7 cols'), (8, '8 cols'), (9, '9 cols'), (10, '10 cols'), (11, '11 cols'), (12, '12 cols')])),
                ('append', models.IntegerField(default=0, verbose_name='Append', choices=[(0, b' \xe2\x80\x94 '), (1, '1 col'), (2, '2 cols'), (3, '3 cols'), (4, '4 cols'), (5, '5 cols'), (6, '6 cols'), (7, '7 cols'), (8, '8 cols'), (9, '9 cols'), (10, '10 cols'), (11, '11 cols'), (12, '12 cols')])),
                ('push', models.IntegerField(default=0, verbose_name='Push', choices=[(0, b' \xe2\x80\x94 '), (1, '1 col'), (2, '2 cols'), (3, '3 cols'), (4, '4 cols'), (5, '5 cols'), (6, '6 cols'), (7, '7 cols'), (8, '8 cols'), (9, '9 cols'), (10, '10 cols'), (11, '11 cols'), (12, '12 cols')])),
                ('pull', models.IntegerField(default=12, verbose_name='Pull', choices=[(0, b' \xe2\x80\x94 '), (1, '1 col'), (2, '2 cols'), (3, '3 cols'), (4, '4 cols'), (5, '5 cols'), (6, '6 cols'), (7, '7 cols'), (8, '8 cols'), (9, '9 cols'), (10, '10 cols'), (11, '11 cols'), (12, '12 cols')])),
                ('vertical_prepend', models.IntegerField(default=0, verbose_name='V. Prepend', choices=[(0, b' \xe2\x80\x94 '), (1, '1 row'), (2, '2 rows'), (3, '3 rows'), (4, '4 rows'), (5, '5 rows'), (6, '6 rows'), (7, '7 rows'), (8, '8 rows'), (9, '9 rows'), (10, '10 rows'), (11, '11 rows'), (12, '12 rows'), (13, '13 rows'), (14, '14 rows'), (15, '15 rows'), (16, '16 rows'), (17, '17 rows'), (18, '18 rows'), (19, '19 rows'), (20, '20 rows'), (21, '21 rows'), (22, '22 rows'), (23, '23 rows'), (24, '24 rows')])),
                ('vertical_append', models.IntegerField(default=0, verbose_name='V. Append', choices=[(0, b' \xe2\x80\x94 '), (1, '1 row'), (2, '2 rows'), (3, '3 rows'), (4, '4 rows'), (5, '5 rows'), (6, '6 rows'), (7, '7 rows'), (8, '8 rows'), (9, '9 rows'), (10, '10 rows'), (11, '11 rows'), (12, '12 rows'), (13, '13 rows'), (14, '14 rows'), (15, '15 rows'), (16, '16 rows'), (17, '17 rows'), (18, '18 rows'), (19, '19 rows'), (20, '20 rows'), (21, '21 rows'), (22, '22 rows'), (23, '23 rows'), (24, '24 rows')])),
                ('vertical_push', models.IntegerField(default=0, verbose_name='V. Push', choices=[(0, b' \xe2\x80\x94 '), (1, '1 row'), (2, '2 rows'), (3, '3 rows'), (4, '4 rows'), (5, '5 rows'), (6, '6 rows'), (7, '7 rows'), (8, '8 rows'), (9, '9 rows'), (10, '10 rows'), (11, '11 rows'), (12, '12 rows'), (13, '13 rows'), (14, '14 rows'), (15, '15 rows'), (16, '16 rows'), (17, '17 rows'), (18, '18 rows'), (19, '19 rows'), (20, '20 rows'), (21, '21 rows'), (22, '22 rows'), (23, '23 rows'), (24, '24 rows')])),
                ('vertical_pull', models.IntegerField(default=0, verbose_name='V. Pull', choices=[(0, b' \xe2\x80\x94 '), (1, '1 row'), (2, '2 rows'), (3, '3 rows'), (4, '4 rows'), (5, '5 rows'), (6, '6 rows'), (7, '7 rows'), (8, '8 rows'), (9, '9 rows'), (10, '10 rows'), (11, '11 rows'), (12, '12 rows'), (13, '13 rows'), (14, '14 rows'), (15, '15 rows'), (16, '16 rows'), (17, '17 rows'), (18, '18 rows'), (19, '19 rows'), (20, '20 rows'), (21, '21 rows'), (22, '22 rows'), (23, '23 rows'), (24, '24 rows')])),
                ('style', models.IntegerField(default=0, verbose_name='Style', choices=[(0, 'none'), (1, 'nested_box'), (2, 'padded'), (3, 'single box'), (4, 'box top'), (5, 'box middle'), (6, 'box bottom')])),
                ('border', models.IntegerField(default=0, verbose_name='Border', choices=[(0, 'no border'), (1, 'border'), (2, 'wide border')])),
                ('clear', models.IntegerField(default=0, verbose_name='Clear', choices=[(0, 'none'), (1, 'break before'), (2, 'break after')])),
                ('last', models.NullBooleanField(verbose_name='Is last?')),
                ('visible', models.NullBooleanField(verbose_name='Is visible?')),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('parent', models.ForeignKey(related_name='blogcategorieswidget_set', to='web.Page')),
            ],
            options={
                'ordering': ['ordering'],
                'abstract': False,
                'verbose_name_plural': 'blog categories',
                'db_table': 'web_page_blogcategorieswidget',
                'verbose_name': 'blog categories',
                'permissions': [],
            },
            bases=(models.Model, feincms.extensions.ExtensionsMixin),
        ),
        migrations.CreateModel(
            name='RecentBlogPostsWidget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('options', django_extensions.db.fields.json.JSONField(verbose_name='widget options', editable=False, blank=True)),
                ('prerendered_content', models.TextField(verbose_name='prerendered content', editable=False, blank=True)),
                ('label', models.CharField(max_length=255, null=True, verbose_name='Title', blank=True)),
                ('template_name', models.CharField(default=b'default.html', max_length=255, verbose_name='Display')),
                ('span', models.IntegerField(default=12, verbose_name='Span', choices=[(0, b' \xe2\x80\x94 '), (1, '1 col'), (2, '2 cols'), (3, '3 cols'), (4, '4 cols'), (5, '5 cols'), (6, '6 cols'), (7, '7 cols'), (8, '8 cols'), (9, '9 cols'), (10, '10 cols'), (11, '11 cols'), (12, '12 cols')])),
                ('vertical_span', models.IntegerField(default=12, verbose_name='V. Span', choices=[(0, b' \xe2\x80\x94 '), (1, '1 row'), (2, '2 rows'), (3, '3 rows'), (4, '4 rows'), (5, '5 rows'), (6, '6 rows'), (7, '7 rows'), (8, '8 rows'), (9, '9 rows'), (10, '10 rows'), (11, '11 rows'), (12, '12 rows'), (13, '13 rows'), (14, '14 rows'), (15, '15 rows'), (16, '16 rows'), (17, '17 rows'), (18, '18 rows'), (19, '19 rows'), (20, '20 rows'), (21, '21 rows'), (22, '22 rows'), (23, '23 rows'), (24, '24 rows')])),
                ('align', models.IntegerField(default=0, verbose_name='Alignment', choices=[(0, 'auto'), (1, 'left'), (2, 'center'), (3, 'right')])),
                ('vertical_align', models.IntegerField(default=0, verbose_name='V. Alignment', choices=[(0, 'auto'), (1, 'top'), (2, 'middle'), (3, 'bottom')])),
                ('prepend', models.IntegerField(default=12, verbose_name='Prepend', choices=[(0, b' \xe2\x80\x94 '), (1, '1 col'), (2, '2 cols'), (3, '3 cols'), (4, '4 cols'), (5, '5 cols'), (6, '6 cols'), (7, '7 cols'), (8, '8 cols'), (9, '9 cols'), (10, '10 cols'), (11, '11 cols'), (12, '12 cols')])),
                ('append', models.IntegerField(default=0, verbose_name='Append', choices=[(0, b' \xe2\x80\x94 '), (1, '1 col'), (2, '2 cols'), (3, '3 cols'), (4, '4 cols'), (5, '5 cols'), (6, '6 cols'), (7, '7 cols'), (8, '8 cols'), (9, '9 cols'), (10, '10 cols'), (11, '11 cols'), (12, '12 cols')])),
                ('push', models.IntegerField(default=0, verbose_name='Push', choices=[(0, b' \xe2\x80\x94 '), (1, '1 col'), (2, '2 cols'), (3, '3 cols'), (4, '4 cols'), (5, '5 cols'), (6, '6 cols'), (7, '7 cols'), (8, '8 cols'), (9, '9 cols'), (10, '10 cols'), (11, '11 cols'), (12, '12 cols')])),
                ('pull', models.IntegerField(default=12, verbose_name='Pull', choices=[(0, b' \xe2\x80\x94 '), (1, '1 col'), (2, '2 cols'), (3, '3 cols'), (4, '4 cols'), (5, '5 cols'), (6, '6 cols'), (7, '7 cols'), (8, '8 cols'), (9, '9 cols'), (10, '10 cols'), (11, '11 cols'), (12, '12 cols')])),
                ('vertical_prepend', models.IntegerField(default=0, verbose_name='V. Prepend', choices=[(0, b' \xe2\x80\x94 '), (1, '1 row'), (2, '2 rows'), (3, '3 rows'), (4, '4 rows'), (5, '5 rows'), (6, '6 rows'), (7, '7 rows'), (8, '8 rows'), (9, '9 rows'), (10, '10 rows'), (11, '11 rows'), (12, '12 rows'), (13, '13 rows'), (14, '14 rows'), (15, '15 rows'), (16, '16 rows'), (17, '17 rows'), (18, '18 rows'), (19, '19 rows'), (20, '20 rows'), (21, '21 rows'), (22, '22 rows'), (23, '23 rows'), (24, '24 rows')])),
                ('vertical_append', models.IntegerField(default=0, verbose_name='V. Append', choices=[(0, b' \xe2\x80\x94 '), (1, '1 row'), (2, '2 rows'), (3, '3 rows'), (4, '4 rows'), (5, '5 rows'), (6, '6 rows'), (7, '7 rows'), (8, '8 rows'), (9, '9 rows'), (10, '10 rows'), (11, '11 rows'), (12, '12 rows'), (13, '13 rows'), (14, '14 rows'), (15, '15 rows'), (16, '16 rows'), (17, '17 rows'), (18, '18 rows'), (19, '19 rows'), (20, '20 rows'), (21, '21 rows'), (22, '22 rows'), (23, '23 rows'), (24, '24 rows')])),
                ('vertical_push', models.IntegerField(default=0, verbose_name='V. Push', choices=[(0, b' \xe2\x80\x94 '), (1, '1 row'), (2, '2 rows'), (3, '3 rows'), (4, '4 rows'), (5, '5 rows'), (6, '6 rows'), (7, '7 rows'), (8, '8 rows'), (9, '9 rows'), (10, '10 rows'), (11, '11 rows'), (12, '12 rows'), (13, '13 rows'), (14, '14 rows'), (15, '15 rows'), (16, '16 rows'), (17, '17 rows'), (18, '18 rows'), (19, '19 rows'), (20, '20 rows'), (21, '21 rows'), (22, '22 rows'), (23, '23 rows'), (24, '24 rows')])),
                ('vertical_pull', models.IntegerField(default=0, verbose_name='V. Pull', choices=[(0, b' \xe2\x80\x94 '), (1, '1 row'), (2, '2 rows'), (3, '3 rows'), (4, '4 rows'), (5, '5 rows'), (6, '6 rows'), (7, '7 rows'), (8, '8 rows'), (9, '9 rows'), (10, '10 rows'), (11, '11 rows'), (12, '12 rows'), (13, '13 rows'), (14, '14 rows'), (15, '15 rows'), (16, '16 rows'), (17, '17 rows'), (18, '18 rows'), (19, '19 rows'), (20, '20 rows'), (21, '21 rows'), (22, '22 rows'), (23, '23 rows'), (24, '24 rows')])),
                ('style', models.IntegerField(default=0, verbose_name='Style', choices=[(0, 'none'), (1, 'nested_box'), (2, 'padded'), (3, 'single box'), (4, 'box top'), (5, 'box middle'), (6, 'box bottom')])),
                ('border', models.IntegerField(default=0, verbose_name='Border', choices=[(0, 'no border'), (1, 'border'), (2, 'wide border')])),
                ('clear', models.IntegerField(default=0, verbose_name='Clear', choices=[(0, 'none'), (1, 'break before'), (2, 'break after')])),
                ('last', models.NullBooleanField(verbose_name='Is last?')),
                ('visible', models.NullBooleanField(verbose_name='Is visible?')),
                ('post_count', models.PositiveIntegerField(default=3, verbose_name='post count')),
                ('show_button', models.BooleanField(default=True, verbose_name='show link button')),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('parent', models.ForeignKey(related_name='recentblogpostswidget_set', to='web.Page')),
            ],
            options={
                'ordering': ['ordering'],
                'abstract': False,
                'verbose_name_plural': 'recent blog posts',
                'db_table': 'web_page_recentblogpostswidget',
                'verbose_name': 'recent blog posts',
                'permissions': [],
            },
            bases=(models.Model, feincms.extensions.ExtensionsMixin),
        ),
        migrations.RemoveField(
            model_name='breadcrumbswidget',
            name='parent',
        ),
        migrations.DeleteModel(
            name='BreadcrumbsWidget',
        ),
        migrations.RemoveField(
            model_name='contentnavigationwidget',
            name='parent',
        ),
        migrations.DeleteModel(
            name='ContentNavigationWidget',
        ),
        migrations.RemoveField(
            model_name='contextnavigationwidget',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='contextnavigationwidget',
            name='root',
        ),
        migrations.DeleteModel(
            name='ContextNavigationWidget',
        ),
        migrations.RemoveField(
            model_name='languageselectorwidget',
            name='parent',
        ),
        migrations.DeleteModel(
            name='LanguageSelectorWidget',
        ),
        migrations.RemoveField(
            model_name='linearnavigationwidget',
            name='parent',
        ),
        migrations.DeleteModel(
            name='LinearNavigationWidget',
        ),
        migrations.RemoveField(
            model_name='sitemapwidget',
            name='parent',
        ),
        migrations.DeleteModel(
            name='SiteMapWidget',
        ),
        migrations.RemoveField(
            model_name='sitesearchwidget',
            name='parent',
        ),
        migrations.DeleteModel(
            name='SiteSearchWidget',
        ),
        migrations.RemoveField(
            model_name='treenavigationwidget',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='treenavigationwidget',
            name='root',
        ),
        migrations.DeleteModel(
            name='TreeNavigationWidget',
        ),
        migrations.AlterField(
            model_name='applicationwidget',
            name='urlconf_path',
            field=models.CharField(max_length=100, verbose_name='application', choices=[(b'elephantblog.urls', b'Blog')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='htmltextwidget',
            name='text',
            field=models.TextField(default=b'<p><django.utils.functional.__proxy__ object at 0x7faa13fdb250></p>', verbose_name='text', blank=True),
            preserve_default=True,
        ),
    ]
