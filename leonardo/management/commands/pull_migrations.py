
from __future__ import unicode_literals

import os
import shutil
from optparse import make_option

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand, NoArgsCommand
from importlib import import_module


class Command(BaseCommand):

    help = "Iterate over all application and copy migrations into site"
    option_list = NoArgsCommand.option_list + (
        make_option('--apps',
                    action='store_false', dest='interactive', default=[],
                    help="Apps for updating as array delimeted with comma."),
    )

    def handle(self, *args, **options):

        skipped_paths = []
        pull_apps = []

        if len(args) > 0:
            app_names = args[0]
            if not isinstance(app_names, list):
                app_names = app_names.split(',')

                _apps = []
                for app_name in app_names:
                    try:
                        app = apps.get_app_config(app_name)
                    except:
                        skipped_paths(app_name)
                    else:
                        _apps.append(app.path)
        else:
            for app in apps.get_app_configs():
                for migration_name in settings.MIGRATION_MODULES.keys():
                    if app.name == migration_name:
                        if app not in pull_apps:
                            pull_apps.append(app)

        def copytree(src, dst, symlinks=False, ignore=None):
            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(dst, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, symlinks, ignore)
                else:
                    shutil.copy2(s, d)

        for app in pull_apps:
            module_name = settings.MIGRATION_MODULES[app.name]
            migration_path = import_module(module_name).__path__[0]

            self.stdout.write("Copy %s to %s" % (app.path, migration_path))

            if os.path.exists(os.path.join(app.path, 'migrations')):
                copytree(os.path.join(app.path, 'migrations'), migration_path)

        self.stdout.write('Successfully pulled %s' % [app.name
                                                      for app in pull_apps])
