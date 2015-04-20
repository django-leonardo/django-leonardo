from __future__ import unicode_literals

import codecs
import os
from collections import OrderedDict
from optparse import make_option

from django.contrib.staticfiles.finders import get_finders
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files.storage import FileSystemStorage
from django.core.management.base import BaseCommand, CommandError
from django.core.management.color import no_style
from django.utils.encoding import smart_text
from django.utils.six.moves import input
from leonardo.module.web.models import PageColorScheme, PageTheme
from django.core.management.base import CommandError, NoArgsCommand

from .sync_widget_themes import Command as SyncWidgetsCommand
from .sync_page_themes import Command as PageThemeCommand

from leonardo.module.web.models import PageTheme

from ._utils import get_or_create_template


class Command(BaseCommand):

    help = "Syncs templates and themes"
    option_list = NoArgsCommand.option_list + (
        make_option("-f", "--force",
                    action="store_true", dest="force", default=False,
                    help="overwrite existing database templates"),
        make_option('--noinput',
                            action='store_false', dest='interactive', default=True,
                            help="Do NOT prompt the user for input of any kind."),
        )

    def handle(self, **options):
        force = options.get('force', False)

        # sync widgets
        sync_cmd = SyncWidgetsCommand()
        sync_cmd.stdout = self.stdout
        sync_cmd.handle(**{
            'force': force,
            'verbosity': False})

        # sync page themes
        sync_cmd = PageThemeCommand()
        sync_cmd.stdout = self.stdout
        sync_cmd.handle(**{
            'force': force,
            'verbosity': False})
