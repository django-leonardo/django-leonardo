from __future__ import unicode_literals

from optparse import make_option

from django.core.management.base import BaseCommand, NoArgsCommand
from .sync_page_themes import Command as PageThemeCommand
from .sync_widget_themes import Command as SyncWidgetsCommand


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
