from __future__ import unicode_literals

from optparse import make_option

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, NoArgsCommand
from .sync_page_themes import Command as PageThemeCommand
from .sync_widget_themes import Command as SyncWidgetsCommand


class Command(BaseCommand):

    help = "Syncs templates and themes"
    option_list = NoArgsCommand.option_list + (
        make_option("-f", "--force",
                    action="store_true", dest="force", default=False,
                    help="overwrite existing database templates"),
        make_option("-n", "--nocompress",
                    action="store_true", dest="nocompress", default=False,
                    help="Without compress command"),
    )

    def handle(self, **options):
        force = options.get('force', False)
        nocompress = options.get('nocompress', True)

        # sync widgets
        sync_cmd = SyncWidgetsCommand()
        sync_cmd.stdout = self.stdout
        self.stdout.write('Syncing widget themes...')
        sync_cmd.handle(**{
            'force': force,
            'verbosity': False})
        self.stdout.write('Syncing widget themes complete.')

        # sync page themes
        self.stdout.write('Syncing page themes...')
        sync_cmd = PageThemeCommand()
        sync_cmd.stdout = self.stdout
        sync_cmd.handle(**{
            'force': force,
            'verbosity': False})
        self.stdout.write('Syncing page themes complete.')

        if settings.COMPRESS_OFFLINE and not nocompress:
            self.stdout.write('Compressing static files...')
            call_command('compress')
            self.stdout.write('Compressing static files complete.')
