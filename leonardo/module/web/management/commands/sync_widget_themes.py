
from django.utils import six
from django.conf import settings
import os
from optparse import make_option

from django.core.management.base import NoArgsCommand
from leonardo.module.web.models import Widget, WidgetContentTheme, WidgetBaseTheme

from ._utils import get_or_create_template

"widget.verbose_name - template.name"
THEME_NAME_FORMAT = "{0} {1}"


class Command(NoArgsCommand):
    help = "Syncs file system templates and themes with the database bidirectionally.\
    based on dbtemplates.sync_templates"
    option_list = NoArgsCommand.option_list + (
        make_option("-f", "--force",
                    action="store_true", dest="force", default=False,
                    help="overwrite existing database templates"),
    )

    def get_all_widget_classes(self):
        """returns collected Leonardo Widgets

        if not declared in settings is used __subclasses__
        which not supports widget subclassing

        """
        _widgets = getattr(settings,
                           'WIDGETS', Widget.__subclasses__())
        widgets = []
        if isinstance(_widgets, dict):
            for group, widget_cls in six.iteritems(_widgets):
                widgets.extend(widget_cls)
        elif isinstance(_widgets, list):
            widgets = _widgets
        return widgets

    def handle_noargs(self, **options):
        force = options.get('force')

        created_themes = 0
        synced_themes = 0

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
                    synced_themes += 1
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
                        created_themes += 1

        # load widget templates and create widget themes with default base
        for w in self.get_all_widget_classes():
            templates = w.templates()
            for name in templates:
                # ignore private members
                if not name.startswith("_"):
                    widget_template = get_or_create_template(name, force=force)
                    synced_themes += 1

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
        self.stdout.write('Successfully synced %s widget themes' % synced_themes)
