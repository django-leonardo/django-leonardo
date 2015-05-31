from __future__ import unicode_literals

from optparse import make_option

from django.core.management.base import BaseCommand, NoArgsCommand
from .sync_page_themes import Command as PageThemeCommand
from .sync_widget_themes import Command as SyncWidgetsCommand


class Command(BaseCommand):

    help = "Scaffold new Site"
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

        from leonardo.module.web.utils.scaffold_web import create_new_site

        page = create_new_site()
