

from django.utils.importlib import import_module
from django.utils import six

BLACKLIST = ['haystack']


class dotdict(dict):

    """ Dictionary with dot access """

    def __getattr__(self, attr):
        return self.get(attr, None)
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def _get_key_from_module(mod, key, default):
    value = getattr(mod, key, default)
    # if not found try second variant
    if value == default:
        value = getattr(mod, 'LEONARDO_%s' % key.upper(), default)
    return value

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

# define options
CONF_SPEC = {
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
}


def extract_conf_from(mod, conf=dotdict(CONF_SPEC)):

    conf['plugins'] = _get_key_from_module(mod, 'plugins', [])
    conf['apps'] = _get_key_from_module(mod, 'apps', [])
    conf['middlewares'] = _get_key_from_module(mod, 'middlewares', [])
    conf['page_extensions'] = _get_key_from_module(mod, 'page_extensions', [])
    conf['auth_backends'] = _get_key_from_module(mod, 'auth_backends', [])
    conf['js_files'] = _get_key_from_module(mod, 'js_files', [])
    conf['angular_modules'] = _get_key_from_module(mod, 'angular_modules', [])
    conf['js_spec_files'] = _get_key_from_module(mod, 'js_spec_files', [])
    conf['css_files'] = _get_key_from_module(mod, 'css_files', [])
    conf['scss_files'] = _get_key_from_module(mod, 'scss_files', [])
    conf['widgets'] = _get_key_from_module(mod, 'widgets', [])
    conf['module_actions'] = _get_key_from_module(mod, 'module_actions', [])
    conf['optgroup'] = _get_key_from_module(mod, 'optgroup',
                                            getattr(
                                                mod,
                                                "__name__",
                                                str(mod)).capitalize())
    conf['config'] = _get_key_from_module(mod, 'config', {})
    conf['absolute_url_overrides'] = _get_key_from_module(
        mod,
        'absolute_url_overrides',
        {})
    conf['migration_modules'] = _get_key_from_module(mod,
                                                     'migration_modules', {})

    conf['navigation_extensions'] = _get_key_from_module(
        mod,
        'navigation_extensions',
        [])
    conf['dirs'] = _get_key_from_module(mod, 'dirs', [])
    conf['context_processors'] = _get_key_from_module(
        mod, 'context_processors', [])

    # support for recursive dependecies
    filtered_apps = [app for app in conf['apps'] if app not in BLACKLIST]
    for app in filtered_apps:
        try:
            app_module = import_module(app)
            if app_module != mod:
                app_module = _get_right_module(app_module)
                mod_conf = extract_conf_from(app_module)
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


def _get_right_module(mod):
    """return imported module
    check if is ``leonardo_module_conf`` specified and then import them
    """

    module_location = getattr(
        mod, 'leonardo_module_conf',
        getattr(mod, "LEONARDO_MODULE_CONF", None))
    if module_location:
        mod = import_module(module_location)
    return mod


def get_conf_from_module(mod):
    """return configuration from module with defaults no worry about None type

    """

    conf = dotdict(CONF_SPEC)

    # get imported module
    mod = _get_right_module(mod)

    # extarct from default object or from module
    if hasattr(mod, 'default'):
        default = mod.default
        conf = extract_conf_from(default, conf)
    else:
        conf = extract_conf_from(mod, conf)
    return conf
