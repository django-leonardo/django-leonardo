
import warnings
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured

default_app_config = 'leonardo.module.search.SearchConfig'


class Default(object):

    optgroup = 'Search'

    @property
    def apps(self):

        INSTALLED_APPS = []
        try:
            import whoosh
        except Exception as e:
            try:
                import haystack
            except ImportError as e:
                warnings.warn(
                    'Haystack search engine is disabled because: {}'.format(e))
            except ImproperlyConfigured as e:
                warnings.warn(
                    'Haystack search engine is disabled because: {}'.format(e))
            else:
                INSTALLED_APPS += ['haystack']
        else:
            INSTALLED_APPS += ['whoosh', 'haystack']

        return INSTALLED_APPS + ['leonardo.module.search']

    plugins = [
        ('leonardo.module.search.apps.search', _('Search'))
    ]


class SearchConfig(AppConfig, Default):
    name = 'leonardo.module.search'
    verbose_name = "Search Module"

default = Default()
