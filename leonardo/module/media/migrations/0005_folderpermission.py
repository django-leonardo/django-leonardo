# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('media', '0004_flash'),
    ]

    operations = [
        migrations.CreateModel(
            name='FolderPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.SmallIntegerField(default=0, verbose_name='type', choices=[(0, 'all items'), (1, 'this item only'), (2, 'this item and all children')])),
                ('everybody', models.BooleanField(default=False, verbose_name='everybody')),
                ('can_edit', models.SmallIntegerField(default=None, null=True, verbose_name='can edit', blank=True, choices=[(1, 'allow'), (0, 'deny')])),
                ('can_read', models.SmallIntegerField(default=None, null=True, verbose_name='can read', blank=True, choices=[(1, 'allow'), (0, 'deny')])),
                ('can_add_children', models.SmallIntegerField(default=None, null=True, verbose_name='can add children', blank=True, choices=[(1, 'allow'), (0, 'deny')])),
                ('folder', models.ForeignKey(related_name='media_folder_permissions', verbose_name=b'folder', blank=True, to='media.LeonardoFolder', null=True)),
                ('group', models.ForeignKey(related_name='media_folder_permissions', verbose_name='group', blank=True, to='auth.Group', null=True)),
                ('user', models.ForeignKey(related_name='media_folder_permissions', verbose_name='user', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'folder permission',
                'verbose_name_plural': 'folder permissions',
            },
            bases=(models.Model,),
        ),
    ]
