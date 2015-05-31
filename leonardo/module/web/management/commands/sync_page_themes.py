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
    help = "Collect static files in a single location."
    requires_system_checks = False

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.copied_files = []
        self.symlinked_files = []
        self.unmodified_files = []
        self.post_processed_files = []
        self.storage = staticfiles_storage
        self.style = no_style()
        try:
            self.storage.path('')
        except NotImplementedError:
            self.local = False
        else:
            self.local = True

    def add_arguments(self, parser):
        parser.add_argument('--noinput',
                            action='store_false', dest='interactive', default=True,
                            help="Do NOT prompt the user for input of any kind.")
        parser.add_argument('--no-post-process',
                            action='store_false', dest='post_process', default=True,
                            help="Do NOT post process collected files.")
        parser.add_argument('-i', '--ignore', action='append', default=[],
                            dest='ignore_patterns', metavar='PATTERN',
                            help="Ignore files or directories matching this glob-style "
                            "pattern. Use multiple times to ignore more.")
        parser.add_argument('-n', '--dry-run',
                            action='store_true', dest='dry_run', default=False,
                            help="Do everything except modify the filesystem.")
        parser.add_argument('-c', '--clear',
                            action='store_true', dest='clear', default=False,
                            help="Clear the existing files using the storage "
                            "before trying to copy or link the original file.")
        parser.add_argument('-l', '--link',
                            action='store_true', dest='link', default=False,
                            help="Create a symbolic link to each file instead of copying.")
        parser.add_argument('--no-default-ignore', action='store_false',
                            dest='use_default_ignore_patterns', default=True,
                            help="Don't ignore the common private glob-style patterns 'CVS', "
                            "'.*' and '*~'.")

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

        self.stdout.write(
            'Successfully synced {} page themes'.format(page_themes))

        message = ['\n']

        if self.is_local_storage() and self.storage.location:
            destination_path = self.storage.location
            message.append(':\n\n    %s\n\n' % destination_path)
        else:
            destination_path = None
            message.append('.\n\n')

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
                'verbosity': 1})

        collected = self.collect()

        self.stdout.write("Page themes synced {}".format(self.page_themes_updated))
        self.stdout.write("Page Skins synced {}".format(self.skins_updated))

    def log(self, msg, level=2):
        """
        Small log helper
        """
        if self.verbosity >= level:
            self.stdout.write(msg)

    def is_local_storage(self):
        return isinstance(self.storage, FileSystemStorage)

    def clear_dir(self, path):
        """
        Deletes the given relative path using the destination storage backend.
        """
        if not self.storage.exists(path):
            return

        dirs, files = self.storage.listdir(path)
        for f in files:
            fpath = os.path.join(path, f)
            if self.dry_run:
                self.log("Pretending to delete '%s'" %
                         smart_text(fpath), level=1)
            else:
                self.log("Deleting '%s'" % smart_text(fpath), level=1)
                self.storage.delete(fpath)
        for d in dirs:
            self.clear_dir(os.path.join(path, d))

    def delete_file(self, path, prefixed_path, source_storage):
        """
        Checks if the target file should be deleted if it already exists
        """
        if self.storage.exists(prefixed_path):
            try:
                # When was the target file modified last time?
                target_last_modified = \
                    self.storage.modified_time(prefixed_path)
            except (OSError, NotImplementedError, AttributeError):
                # The storage doesn't support ``modified_time`` or failed
                pass
            else:
                try:
                    # When was the source file modified last time?
                    source_last_modified = source_storage.modified_time(path)
                except (OSError, NotImplementedError, AttributeError):
                    pass
                else:
                    # The full path of the target file
                    if self.local:
                        full_path = self.storage.path(prefixed_path)
                    else:
                        full_path = None
                    # Skip the file if the source file is younger
                    # Avoid sub-second precision (see #14665, #19540)
                    if (target_last_modified.replace(microsecond=0)
                            >= source_last_modified.replace(microsecond=0)):
                        if not ((self.symlink and full_path
                                 and not os.path.islink(full_path)) or
                                (not self.symlink and full_path
                                 and os.path.islink(full_path))):
                            if prefixed_path not in self.unmodified_files:
                                self.unmodified_files.append(prefixed_path)
                            self.log("Skipping '%s' (not modified)" % path)
                            return False
            # Then delete the existing file if really needed
            if self.dry_run:
                self.log("Pretending to delete '%s'" % path)
            else:
                self.log("Deleting '%s'" % path)
                self.storage.delete(prefixed_path)
        return True

    def link_file(self, path, prefixed_path, source_storage):
        """
        Attempt to link ``path``
        """
        # Skip this file if it was already copied earlier
        if prefixed_path in self.symlinked_files:
            return self.log("Skipping '%s' (already linked earlier)" % path)
        # Delete the target file if needed or break
        if not self.delete_file(path, prefixed_path, source_storage):
            return
        # The full path of the source file
        source_path = source_storage.path(path)
        # Finally link the file
        if self.dry_run:
            self.log("Pretending to link '%s'" % source_path, level=1)
        else:
            self.log("Linking '%s'" % source_path, level=1)
            full_path = self.storage.path(prefixed_path)
            try:
                os.makedirs(os.path.dirname(full_path))
            except OSError:
                pass
            try:
                if os.path.lexists(full_path):
                    os.unlink(full_path)
                os.symlink(source_path, full_path)
            except AttributeError:
                import platform
                raise CommandError("Symlinking is not supported by Python %s." %
                                   platform.python_version())
            except NotImplementedError:
                import platform
                raise CommandError("Symlinking is not supported in this "
                                   "platform (%s)." % platform.platform())
            except OSError as e:
                raise CommandError(e)
        if prefixed_path not in self.symlinked_files:
            self.symlinked_files.append(prefixed_path)

    def copy_file(self, path, prefixed_path, source_storage):
        """
        Attempt to copy ``path`` with storage
        """
        # Skip this file if it was already copied earlier
        if prefixed_path in self.copied_files:
            return self.log("Skipping '%s' (already copied earlier)" % path)
        # Delete the target file if needed or break
        if not self.delete_file(path, prefixed_path, source_storage):
            return
        # The full path of the source file
        source_path = source_storage.path(path)
        # Finally start copying
        if self.dry_run:
            self.log("Pretending to copy '%s'" % source_path, level=1)
        else:
            self.log("Copying '%s'" % source_path, level=1)
            with source_storage.open(path) as source_file:
                self.storage.save(prefixed_path, source_file)
        self.copied_files.append(prefixed_path)
