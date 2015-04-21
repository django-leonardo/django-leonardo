
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
        overwrite = options.get('overwrite')

        # base
        path = os.path.dirname(os.path.abspath(__file__))
        possible_topdir = os.path.normpath(os.path.join(path,
                                                        os.pardir,
                                                        os.pardir,
                                                        "templates"))

        # load widget base templates
        widget_base_dir = os.path.join(possible_topdir, "base", "widget")

        for dirpath, subdirs, filenames in os.walk(widget_base_dir):
            for f in filenames:
                # ignore private members
                if not f.startswith("_"):
                    w_base_template = get_or_create_template(
                        f, force=force, prefix="base/widget")
                    name = f.split("/")[-1].split(".")[0]
                    try:
                        widget_theme = WidgetBaseTheme.objects.get(
                            name__exact=name)
                    except WidgetBaseTheme.DoesNotExist:
                        widget_theme = WidgetBaseTheme()
                        widget_theme.name = name
                        widget_theme.label = name.split(".")[0].title()
                        widget_theme.template = w_base_template
                        widget_theme.save()

        created_themes = 0

        # load widget templates and create widget themes with default base
        for w in Widget.__subclasses__():
            templates = w.templates()
            for name in templates:
                # ignore private members
                if not name.startswith("_"):
                    widget_template = get_or_create_template(name, force=force)

                    if not widget_template:
                        self.stdout.write('Template for "%s" not found' % name)
                        continue

                    try:
                        widget_theme = WidgetContentTheme.objects.get(
                            template__name__exact=name)
                    except WidgetContentTheme.DoesNotExist:
                        widget_theme = WidgetContentTheme()
                        widget_theme.name = name.split("/")[-1].split(".")[0]
                        widget_theme.label = THEME_NAME_FORMAT.format(
                            unicode(w._meta.verbose_name),
                            name.split("/")[-1].split(".")[0]).capitalize()
                        widget_theme.template = widget_template
                        widget_theme.widget_class = w.__name__
                        widget_theme.save()
                        created_themes += 1

        self.stdout.write('Successfully created %s widget themes' % created_themes)
