
import logging

from django.utils.importlib import import_module
from django.utils import six

BLACKLIST = ['haystack']

LOG = logging.getLogger(__name__)


class dotdict(dict):
    """ Dictionary with dot access """

    def __getattr__(self, attr):
        return self.get(attr, None)
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

CONFIG_VALID = (list, tuple)


def merge(a, b):
    """return merged tuples or lists without duplicates
    note: ensure if admin theme is before admin
    """
    if isinstance(a, CONFIG_VALID) \
            and isinstance(b, CONFIG_VALID):
        _a = list(a)
        for x in list(b):
            if x not in _a:
                _a.append(x)
        return _a
    if a and b:
        raise Exception("Cannot merge")
    return None


def get_leonardo_modules():
    """return all leonardo modules

    check every installed module for leonardo descriptor

    """

    modules = []

    try:
        import pip
        installed_packages = pip.get_installed_distributions()
    except Exception as e:
        LOG.exception(e)
        installed_packages = []

    for package in installed_packages:
        # check for default descriptor
        pkg_name = [k for k in package._get_metadata("top_level.txt")][0]
        if pkg_name not in BLACKLIST:
            try:
                mod = import_module(pkg_name)
                if hasattr(mod, 'default'):
                    modules.append(mod)
            except Exception as e:
                LOG.exception(e)

    return modules


def get_conf_from_module(mod):
    """return configuration from module with defaults no worry about None type

    """

    # define options
    conf = dotdict({
        'optgroup': None,
        'plugins': [],
        'widgets': [],
        'apps': [],
        'middlewares': [],
        'context_processors': [],
        'dirs': [],
        'page_extensions': [],
        'auth_backends': [],
        'js_files': [],
        'js_spec_files': [],
        'css_files': [],
        'config': {},
    })

    if hasattr(mod, 'default'):

        conf['plugins'] = getattr(mod.default, 'plugins', [])
        conf['apps'] = getattr(mod.default, 'apps', [])
        conf['middlewares'] = getattr(mod.default, 'middlewares', [])
        conf['page_extensions'] = getattr(mod.default, 'page_extensions', [])
        conf['auth_backends'] = getattr(mod.default, 'auth_backends', [])
        conf['js_files'] = getattr(mod.default, 'js_files', [])
        conf['js_spec_files'] = getattr(mod.default, 'js_spec_files', [])
        conf['css_files'] = getattr(mod.default, 'css_files', [])
        conf['widgets'] = getattr(mod.default, 'widgets', [])
        conf['optgroup'] = getattr(mod.default, 'optgroup', None)
        conf['config'] = getattr(mod.default, 'config', {})

        conf['dirs'] = getattr(mod.default, 'dirs', [])
        conf['context_processors'] = getattr(
            mod.default, 'context_processors', [])

        # support for recursive dependecies
        filtered_apps = [app for app in conf['apps'] if app not in BLACKLIST]
        for app in filtered_apps:
            try:
                app_module = import_module(app)
                if app_module != mod:
                    mod_conf = get_conf_from_module(app_module)
                    for k, v in six.iteritems(mod_conf):
                        if isinstance(v, dict):
                            conf[k].update(v)
                        else:
                            conf[k] = merge(conf[k], v)
            except Exception:
                pass  # swallow, but maybe log for info what happens

    return conf
