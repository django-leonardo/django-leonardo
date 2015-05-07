
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


default_app_config = 'leonardo.module.search.SearchConfig'


class Default(object):

    optgroup = 'Search'

    @property
    def apps(self):

        INSTALLED_APPS = []
        try:
            import whoosh  # noqa
            INSTALLED_APPS += ['whoosh']
        except Exception:
            pass

        return INSTALLED_APPS + ['haystack', 'leonardo.module.search']

    plugins = [
        ('leonardo.module.search.apps.search', _('Search'))
    ]

class SearchConfig(AppConfig, Default):
    name = 'leonardo.module.search'
    verbose_name = "Search Module"

default = Default()
