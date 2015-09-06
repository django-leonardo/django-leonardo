
from __future__ import unicode_literals

import os
from optparse import make_option

from django.apps import apps
from django.core.management import call_command
from django.core.management.base import BaseCommand, NoArgsCommand


class Command(BaseCommand):

    help = "Iterate over all application and generate-compile all translations"
    option_list = NoArgsCommand.option_list + (
        make_option('--apps',
                    action='store_false', dest='interactive', default=[],
                    help="Apps for updating as array delimeted with comma."),
    )

    def handle(self, *args, **options):

        skipped_paths = []

        if len(args) > 0:
            app_names = args[0]
            if not isinstance(app_names, list):
                app_names = app_names.split(',')

                _apps = []
                for app_name in app_names:
                    try:
                        app = apps.get_app_config(app_name)
                    except Exception as e:
                        skipped_paths(app_name)
                    else:
                        _apps.append(app.path)
        else:
            _apps = apps.get_app_paths()

        for app_path in _apps:
            try:
                os.chdir(app_path)
                call_command('makemessages')
                call_command('compilemessages')
            except Exception as e:
                skipped_paths.append(app_path)
                self.stderr.write(str(e))

        if skipped_paths:
            self.stderr.write('Skipped paths: \n%s' % '\n'.join(skipped_paths))
        self.stdout.write('Successfully generated and compiled all messages')
