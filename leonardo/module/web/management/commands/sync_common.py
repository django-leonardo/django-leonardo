
from optparse import make_option

from django.core.management.base import NoArgsCommand

from ._utils import get_or_create_template


class Command(NoArgsCommand):
    help = """Syncs file system templates and themes 
            with the database bidirectionally.
            based on dbtemplates.sync_templates"""

    option_list = NoArgsCommand.option_list + (
        make_option("-f", "--force",
                    action="store_true", dest="force", default=False,
                    help="overwrite existing database templates"),
    )

    def handle_noargs(self, **options):
        force = options.get('force')

        get_or_create_template("404.html", force=force, notfix='admin')
        get_or_create_template("403.html", force=force, notfix='admin')
        get_or_create_template("500.html", force=force, notfix='admin')
        get_or_create_template(
            "crossdomain.xml", force=force, extension='.xml')
        get_or_create_template("robots.txt", force=force, extension='.txt')

        self.stdout.write('Successfully synced common templates '
                          '(404.html, 403.html, 500.html, crossdomain.txt, robots.txt)')
