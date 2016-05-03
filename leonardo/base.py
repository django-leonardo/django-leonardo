
import warnings

from app_loader.base import AppLoader
from django.conf.urls import include, patterns, url
from django.utils import six
from django.utils.functional import cached_property
from django.utils.module_loading import module_has_submodule  # noqa
from importlib import import_module  # noqa
from leonardo.conf import Default
from leonardo.decorators import _decorate_urlconf, require_auth
from leonardo.utils import is_leonardo_module
from leonardo.utils.settings import (get_conf_from_module,
                                     get_loaded_modules,
                                     merge)


# use leonardo instead
default = Default()


class Leonardo(AppLoader):

    '''Main CMS instance

    .. code-block:: python

        from leonardo import leonardo

        print(leonardo.config.apps)
        print(leonardo.config.widgets)
    '''

    default = default

    MODULES_AUTOLOAD = True

    CONFIG_MODULE_PREFIX = "LEONARDO"
    CONFIG_MODULE_SPEC_CLASS = "leonardo.conf.spec.CONF_SPEC"
    CONFIG_MODULE_OBJECT_CLASS = "leonardo.conf.base.ModuleConfig"
    CONFIG_MASTER_OBJECT_CLASS = "leonardo.conf.base.LeonardoConfig"

    def get_app_modules(self, apps):
        """return array of imported leonardo modules for apps
        """
        modules = getattr(self, "_modules", [])

        if not modules:
            from django.utils.module_loading import module_has_submodule

            # Try importing a modules from the module package
            package_string = '.'.join(['leonardo', 'module'])

            for app in apps:
                exc = '...'
                try:
                    # check if is not full app
                    _app = import_module(app)
                except Exception as e:
                    _app = False
                    exc = e

                if module_has_submodule(
                        import_module(package_string), app) or _app:
                    if _app:
                        mod = _app
                    else:
                        mod = import_module('.{0}'.format(app), package_string)
                    if mod:
                        modules.append(mod)
                        continue

                warnings.warn('%s was skipped because %s ' % (app, exc))

            self._modules = modules
        return self._modules

    @cached_property
    def urlpatterns(self):
        '''load and decorate urls from all modules
        then store it as cached property for less loading
        '''
        if not hasattr(self, '_urlspatterns'):
            urlpatterns = []
            # load all urls
            # support .urls file and urls_conf = 'elephantblog.urls' on default module
            # decorate all url patterns if is not explicitly excluded
            for mod in leonardo.modules:
                # TODO this not work
                if is_leonardo_module(mod):

                    conf = get_conf_from_module(mod)

                    if module_has_submodule(mod, 'urls'):
                        urls_mod = import_module('.urls', mod.__name__)
                        if hasattr(urls_mod, 'urlpatterns'):
                            # if not public decorate all

                            if conf['public']:
                                urlpatterns += urls_mod.urlpatterns
                            else:
                                _decorate_urlconf(urls_mod.urlpatterns,
                                                  require_auth)
                                urlpatterns += urls_mod.urlpatterns
            # avoid circural dependency
            # TODO use our loaded modules instead this property
            from django.conf import settings
            for urls_conf, conf in six.iteritems(getattr(settings, 'MODULE_URLS', {})):
                # is public ?
                try:
                    if conf['is_public']:
                        urlpatterns += \
                            patterns('',
                                     url(r'', include(urls_conf)),
                                     )
                    else:
                        _decorate_urlconf(
                            url(r'', include(urls_conf)),
                            require_auth)
                        urlpatterns += patterns('',
                                                url(r'', include(urls_conf)))
                except Exception as e:
                    raise Exception('raised %s during loading %s' %
                                    (str(e), urls_conf))

            self._urlpatterns = urlpatterns

        return self._urlpatterns

    _instance = None

leonardo = Leonardo()
