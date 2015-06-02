

from django.utils.importlib import import_module
from django.utils import six

BLACKLIST = ['haystack']


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
    except Exception:
        installed_packages = []

    for package in installed_packages:
        # check for default descriptor
        pkg_names = [k for k in package._get_metadata("top_level.txt")]
        for pkg_name in pkg_names:
            if pkg_name not in BLACKLIST:
                try:
                    mod = import_module(pkg_name)
                    if hasattr(mod, 'default'):
                        modules.append(mod)
                except Exception:
                    pass

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
        'angular_modules': [],
        'css_files': [],
        'scss_files': [],
        'config': {},
        'migration_modules': {},
        'absolute_url_overrides': {},
        'navigation_extensions': [],
        'module_actions': [],
    })

    if hasattr(mod, 'default'):

        default = mod.default

        conf['plugins'] = getattr(default, 'plugins', [])
        conf['apps'] = getattr(default, 'apps', [])
        conf['middlewares'] = getattr(default, 'middlewares', [])
        conf['page_extensions'] = getattr(default, 'page_extensions', [])
        conf['auth_backends'] = getattr(default, 'auth_backends', [])
        conf['js_files'] = getattr(default, 'js_files', [])
        conf['angular_modules'] = getattr(default, 'angular_modules', [])
        conf['js_spec_files'] = getattr(default, 'js_spec_files', [])
        conf['css_files'] = getattr(default, 'css_files', [])
        conf['scss_files'] = getattr(default, 'scss_files', [])
        conf['widgets'] = getattr(default, 'widgets', [])
        conf['module_actions'] = getattr(default, 'module_actions', [])
        conf['optgroup'] = getattr(default, 'optgroup',
                                   mod.__name__.capitalize())
        conf['config'] = getattr(default, 'config', {})
        conf['absolute_url_overrides'] = getattr(
            default, 'absolute_url_overrides', {})
        conf['migration_modules'] = getattr(default, 'migration_modules', {})
        conf['navigation_extensions'] = getattr(
            default, 'navigation_extensions', [])

        conf['dirs'] = getattr(mod.default, 'dirs', [])
        conf['context_processors'] = getattr(
            mod.default, 'context_processors', [])

        # support for recursive dependecies
        filtered_apps = [app for app in conf['apps'] if app not in BLACKLIST]
        for app in filtered_apps:
            try:
                app_module = import_module(app)
                if app_module != mod:
                    if hasattr(app_module, 'default'):
                        mod_conf = get_conf_from_module(app_module)
                        for k, v in six.iteritems(mod_conf):
                            # prevent config duplicity
                            # skip config merge
                            if k == 'config':
                                continue
                            if isinstance(v, dict):
                                conf[k].update(v)
                            elif isinstance(v, (list, tuple)):
                                conf[k] = merge(conf[k], v)
            except Exception:
                pass  # swallow, but maybe log for info what happens

    return conf
