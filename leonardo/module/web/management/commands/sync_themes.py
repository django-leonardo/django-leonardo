import codecs
import os
from optparse import make_option

from django.core.management.base import CommandError, NoArgsCommand
from leonardo.module.web.models import Widget, WidgetTheme, PageTheme

from .utils import get_or_create_template

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
        extension = options.get('ext')
        force = options.get('force')
        overwrite = options.get('overwrite')
        app_first = options.get('app_first')
        delete = options.get('delete')

        # TODO: base template as param
        base_template_name = 'widget/base.html'
        base_template = get_or_create_template(base_template_name)

        created_themes = 0

        for w in Widget.__subclasses__():
            templates = w.templates()
            for name in templates:

                widget_template = get_or_create_template(name)

                if not widget_template:
                    self.stdout.write('Template for "%s" not found' % name)
                    continue

                try:
                    widget_theme = WidgetTheme.objects.get(
                        content_template__name__exact=name)
                except WidgetTheme.DoesNotExist:
                    widget_theme = WidgetTheme()
                    widget_theme.label = THEME_NAME_FORMAT.format(
                        unicode(w._meta.verbose_name), name.split("/")[-1])
                    widget_theme.content_template = widget_template
                    widget_theme.base_template = base_template
                    widget_theme.widget_class = w.__class__.__name__
                    widget_theme.save()
                    created_themes += 1

        self.stdout.write('Successfully created %s widget themes' % created_themes)

        # page theme
        # TODO move to own directory and makes more confrotable
        name = 'layout/page.html'
        page_template = get_or_create_template(name)

        try:
            page_theme = PageTheme.objects.get(
                template__name__exact=name)
        except PageTheme.DoesNotExist:
            page_theme = PageTheme()
            page_theme.label = 'Page layout'
            page_theme.template = page_template
            page_theme.save()

        self.stdout.write('Successfully synced page theme')
