
import os
from optparse import make_option

from django.core.management.base import NoArgsCommand
from leonardo.module.web.models import Widget, WidgetContentTheme, PageTheme, WidgetBaseTheme

from ._utils import get_or_create_template

"widget.verbose_name - template.name"
THEME_NAME_FORMAT = "{0} {1}"


class Command(NoArgsCommand):
    help = "Syncs file system templates and themes with the database bidirectionally.\
    based on dbtemplates.sync_templates"
    option_list = NoArgsCommand.option_list + (
        make_option("-e", "--ext",
                    dest="ext", action="store", default="html",
                    help="extension of the files you want to "
                         "sync with the database [default: %default]"),
        make_option("-f", "--force",
                    action="store_true", dest="force", default=False,
                    help="overwrite existing database templates"),
        make_option("-o", "--overwrite",
                    action="store", dest="overwrite", default='0',
                    help="'0' - ask always, '1' - overwrite database "
                         "templates from template files, '2' - overwrite "
                         "template files from database templates"),
        make_option("-a", "--app-first",
                    action="store_true", dest="app_first", default=False,
                    help="look for templates in applications "
                         "directories before project templates"),
        make_option("-d", "--delete",
                    action="store_true", dest="delete", default=False,
                    help="Delete templates after syncing"))

    def handle_noargs(self, **options):
        force = options.get('force')

        get_or_create_template("404.html", force=force, notfix='admin')
        get_or_create_template("500.html", force=force, notfix='admin')
        get_or_create_template("crossdomain.xml", force=force, extension='.xml')
        get_or_create_template("robots.txt", force=force, extension='.txt')
