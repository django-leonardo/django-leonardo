
from __future__ import unicode_literals

import os
from optparse import make_option

from django.apps import apps
from django.core.management import call_command
from django.core.management.base import BaseCommand, NoArgsCommand


class Command(BaseCommand):

    help = "Iterate over all application and generate-compile all translations"
    option_list = NoArgsCommand.option_list + (
        make_option('--noinput',
                    action='store_false', dest='interactive', default=True,
                    help="Do NOT prompt the user for input of any kind."),
    )

    def handle(self, **options):

        skipped_paths = []

        for app_path in apps.get_app_paths():
            try:
                os.chdir(app_path)
                call_command('makemessages')
                call_command('compilemessages')
            except Exception as e:
                skipped_paths.append(app_path)
                self.stderr.write(str(e))

        if skipped_paths:
            self.stderr.write('Skipped paths %s' % skipped_paths)
        self.stdout.write('Successfully generated and compiled all messages')
