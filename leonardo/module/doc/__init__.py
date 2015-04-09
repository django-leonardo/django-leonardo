
from django.apps import AppConfig

default_app_config = 'leonardo.module.doc.DocumentationConfig'


class Default(object):

    optgroup = ('Documentation')

    @property
    def apps(self):
        return [
            'leonardo.module.doc',
        ]


class DocumentationConfig(AppConfig, Default):
    name = 'leonardo.module.doc'
    verbose_name = "Documentation"

default = Default()
