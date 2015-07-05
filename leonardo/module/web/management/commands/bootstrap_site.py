from __future__ import unicode_literals

from optparse import make_option

from django.core.management.base import BaseCommand, NoArgsCommand
from .sync_page_themes import Command as PageThemeCommand
from .sync_widget_themes import Command as SyncWidgetsCommand
from leonardo.module.web.utils.scaffold_web import create_new_site


class Command(BaseCommand):

    help = "Bootstrap new Site"
    option_list = NoArgsCommand.option_list + (
        make_option("-f", "--force",
                    action="store_true", dest="force", default=False,
                    help="overwrite existing database templates"),
        make_option("-n", "--name",
                    action="store", dest="name", default='demo.yaml',
                    help="script name in LEONARDO_BOOTSTRAP_DIR default is demo.yaml"),
        make_option("-s", "--sync",
                    action="store", dest="sync", default=True,
                    help="Run sync_all -f before load ?"),
        make_option("--url",
                    action="store", dest="url", default=False,
                    help="url for bootstrap source"),
        make_option('--noinput',
                    action='store_false', dest='interactive', default=True,
                    help="Do NOT prompt the user for input of any kind."),
    )

    def handle(self, *args, **options):
        force = options.get('force', False)
        sync = options.get('sync')
        name = options.get('name')
        url = options.get('url', None)
        page = create_new_site(name=name,
                               run_syncall=sync,
                               url=url)

        self.stdout.write('Site {} was successfully loaded.'.format(url or name))
