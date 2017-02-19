# install dependencies

from __future__ import unicode_literals

from leonardo import leonardo
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Install dependencies declared directly in plugin config"

    def handle(self, *args, **options):
        if len(leonardo.config.requirements) > 0:

            from leonardo.utils.package import install_package

            for req in leonardo.config.requirements:
                install_package(req)

            self.stdout.write('Successfully installed %s' % ','.join(
                leonardo.config.requirements))
