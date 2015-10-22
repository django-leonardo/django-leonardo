from __future__ import unicode_literals

import codecs
import os
from collections import OrderedDict

from dbtemplates.conf import settings
from django.contrib.staticfiles.finders import get_finders
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files.storage import FileSystemStorage
from django.core.management.base import BaseCommand, CommandError
from django.core.management.color import no_style
from django.utils.encoding import smart_text
from leonardo.utils.settings import merge
from leonardo.module.web.models import PageColorScheme, PageTheme
from ._utils import app_template_dirs, DIRS, get_or_create_template

from django.contrib.staticfiles.management.commands.collectstatic \
    import Command as CollectStatic


class Command(BaseCommand):

    """
    Command that allows to copy or symlink static files from different
    locations to the settings.STATIC_ROOT.
    """
    help = "Find and load page themes with their color variations."

    def add_arguments(self, parser):
        parser.add_argument('--noinput',
                            action='store_false', dest='interactive', default=True,
                            help="Do NOT prompt the user for input of any kind.")


    def set_options(self, **options):
        """
        Set instance variables based on an options dict
        """
        self.interactive = False
        self.verbosity = options['verbosity']
        self.symlink = ""
        self.clear = False
        ignore_patterns = []
        self.ignore_patterns = list(set(ignore_patterns))
        self.page_themes_updated = 0
        self.skins_updated = 0

    def collect(self):
        """
        Load and save ``PageColorScheme`` for every ``PageTheme``

        .. code-block:: bash

            static/themes/bootswatch/united/variables.scss
            static/themes/bootswatch/united/styles.scss

        """

        self.ignore_patterns = [
            '*.png', '*.jpg', '*.js', '*.gif', '*.ttf', '*.md', '*.rst',
            '*.svg']
        page_themes = PageTheme.objects.all()

        for finder in get_finders():
            for path, storage in finder.list(self.ignore_patterns):
                for t in page_themes:
                    static_path = 'themes/{0}'.format(t.name.split('/')[-1])
                    if static_path in path:
                        try:
                            page_theme = PageTheme.objects.get(id=t.id)
                        except PageTheme.DoesNotExist:
                            raise Exception("Run sync_themes before this command")
                        except Exception as e:
                            self.stdout.write(
                                "Cannot load {} into database original error: {}".format(t, e))

                        # find and load skins
                        skins_path = os.path.join(
                            storage.path('/'.join(path.split('/')[0:-1])))
                        for dirpath, skins, filenames in os.walk(skins_path):
                            for skin in [s for s in skins if s not in ['fonts']]:
                                for skin_dirpath, skins, filenames in os.walk(os.path.join(dirpath, skin)):
                                    skin, created = PageColorScheme.objects.get_or_create(
                                        theme=page_theme, label=skin, name=skin.title())
                                    for f in filenames:
                                        if 'styles' in f:
                                            with codecs.open(os.path.join(skin_dirpath, f)) as style_file:
                                                skin.styles = style_file.read()
                                        elif 'variables' in f:
                                            with codecs.open(os.path.join(skin_dirpath, f)) as variables_file:
                                                skin.variables = variables_file.read()
                                    skin.save()
                                    self.skins_updated += 1

        self.page_themes_updated += len(page_themes)

    def handle(self, **options):
        self.set_options(**options)
        force = options.get('force', False)

        # base
        page_themes = 0

        tpl_dirs = merge(DIRS, app_template_dirs)
        templatedirs = [d for d in tpl_dirs if os.path.isdir(d)]

        for templatedir in templatedirs:
            for dirpath, subdirs, filenames in os.walk(templatedir):
                if 'base/page' in dirpath:
                    for f in filenames:
                        # ignore private and hidden members
                        if not f.startswith("_") and not f.startswith("."):
                            page_template = get_or_create_template(
                                f, force=force, prefix="base/page")
                            if not page_template:
                                self.stdout.write("Missing template %s" % f)
                                continue
                            # create themes with bases
                            try:
                                page_theme = PageTheme.objects.get(
                                    name=f.split(".")[0])
                            except PageTheme.DoesNotExist:
                                page_theme = PageTheme()
                                page_theme.label = '{} layout'.format(
                                    f.split(".")[0].title())
                                page_theme.name = f.split(".")[0]
                                page_theme.template = page_template
                                page_theme.save()
                                page_themes += 1

        if page_themes > 0:
            self.stdout.write(
                'Successfully created {} page themes'.format(page_themes))

        cmd = CollectStatic()
        cmd.stdout = self.stdout
        collect_static = cmd.handle(
            **{'interactive': False,
                'link': False,
                'clear': False,
                'dry_run': False,
                'ignore_patterns': [],
                'use_default_ignore_patterns': True,
                'post_process': True,
                'verbosity': 0})

        collected = self.collect()

        self.stdout.write("Page themes synced {}".format(self.page_themes_updated))
        self.stdout.write("Page Skins synced {}".format(self.skins_updated))
