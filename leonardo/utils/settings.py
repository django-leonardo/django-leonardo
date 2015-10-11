

from importlib import import_module
from django.utils import six
from .versions import get_versions

import warnings

# define options
CONF_SPEC = {
    'optgroup': None,
    'urls_conf': None,
    'public': False,
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
    'page_actions': [],
    'widget_actions': [],
    'ordering': 0,
}

# just MAP - Django - Our spec
DJANGO_CONF = {
    'INSTALLED_APPS': "apps",
    'APPLICATION_CHOICES': "plugins",
    'MIDDLEWARE_CLASSES': "middlewares",
    'AUTHENTICATION_BACKENDS': "auth_backends",
    'PAGE_EXTENSIONS': "page_extensions",
    'ADD_JS_FILES': "js_files",
    'PAGE_EXTENSIONS': "page_extensions",
    'ADD_PAGE_ACTIONS': "page_actions",
    'ADD_WIDGET_ACTIONS': "widget_actions",
    'ADD_CSS_FILES': "css_files",
    'ADD_JS_FILES': "js_files",
    'ADD_JS_SPEC_FILES': "js_spec_files",
    'ADD_SCSS_FILES': "scss_files",
    'ADD_ANGULAR_MODULES': "angular_modules",
    'MIGRATION_MODULES': "migration_modules",
}

BLACKLIST = ['haystack']
LEONARDO_MODULES = None


def get_loaded_modules(modules):
    '''load modules and order it by ordering key'''

    _modules = []
    for mod in modules:
        mod_cfg = get_conf_from_module(mod)

        _modules.append((mod, mod_cfg,))

    _modules = sorted(_modules, key=lambda m: m[1].get('ordering'))

    return _modules


class dotdict(dict):

    """ Dictionary with dot access """

    def __getattr__(self, attr):
        return self.get(attr, None)
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Config(dict):

    """Simple Module Config Object
    encapsulation of dot access dictionary

    use dictionary as constructor

    """

    def get_value(self, key, values):
        '''Accept key of propery and actual values'''
        return merge(values, self.get_property(key))

    def get_property(self, key):
        """Expect Django Conf property"""
        _key = DJANGO_CONF[key]
        return getattr(self, _key, CONF_SPEC[_key])

    @property
    def module_name(self):
        """Module name from module if is set"""
        if hasattr(self, "module"):
            return self.module.__name__
        return None

    @property
    def name(self):
        """Distribution name from module if is set"""
        if hasattr(self, "module"):
            return self.module.__name__.replace('_', '-')
        return None

    @property
    def version(self):
        """return module version"""
        return get_versions([self.module_name]).get(self.module_name, None)

    @property
    def latest_version(self):
        """return latest version if is available"""
        from leonardo_system.pip import check_versions
        return check_versions(True).get(self.name, None).get('new', None)

    @property
    def needs_migrations(self):
        """Indicates whater module needs migrations"""
        # TODO(majklk): also check models etc.
        if len(self.widgets) > 0:
            return True
        return False

    @property
    def needs_sync(self):
        """Indicates whater module needs templates, static etc."""

        affected_attributes = [
            'css_files', 'js_files',
            'scss_files', 'widgets']

        for attr in affected_attributes:
            if len(getattr(self, attr)) > 0:
                return True
        return False

    def set_module(self, module):
        """Just setter for module"""
        setattr(self, "module", module)

    def __getattr__(self, attr):
        return self.get(attr, None)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def _get_key_from_module(mod, key, default):
    if hasattr(mod, key):
        value = getattr(mod, key, default)
    else:
        value = getattr(mod, 'LEONARDO_%s' % key.upper(), default)
    return value

CONFIG_VALID = (list, tuple, dict)


def merge(a, b):
    """return merged tuples or lists without duplicates
    note: ensure if admin theme is before admin
    """
    if isinstance(a, CONFIG_VALID) \
            and isinstance(b, CONFIG_VALID):
        # dict update
        if isinstance(a, dict) and isinstance(b, dict):
            a.update(b)
            return a
        # list update
        _a = list(a)
        for x in list(b):
            if x not in _a:
                _a.append(x)
        return _a
    if a and b:
        raise Exception("Cannot merge")
    raise NotImplementedError


def get_leonardo_modules():
    """return all leonardo modules

    check every installed module for leonardo descriptor

    by default use in memory cache
    """
    global LEONARDO_MODULES

    if not LEONARDO_MODULES:
        modules = []

        try:
            import pip
            installed_packages = pip.get_installed_distributions()
        except Exception:
            installed_packages = []
            warnings.warn(
                'pip is not installed module, scan module is skipped.',
                RuntimeWarning)

        for package in installed_packages:
            # check for default descriptor
            pkg_names = [k for k in package._get_metadata("top_level.txt")]
            for pkg_name in pkg_names:
                if pkg_name not in BLACKLIST:
                    try:
                        mod = import_module(pkg_name)
                        if hasattr(mod, 'default') \
                                or hasattr(mod, 'leonardo_module_conf'):
                            modules.append(mod)
                            continue
                        for key in dir(mod):
                            if 'LEONARDO' in key:
                                modules.append(mod)
                                break
                    except Exception:
                        pass
        LEONARDO_MODULES = modules
    return LEONARDO_MODULES


def extract_conf_from(mod, conf=Config(CONF_SPEC), depth=0, max_depth=2):
    """recursively extract keys from module or object
    by passed config scheme
    """

    # extract config keys from module or object
    for key, default_value in six.iteritems(conf):
        conf[key] = _get_key_from_module(mod, key, default_value)

    # support for recursive dependecies
    try:
        filtered_apps = [app for app in conf['apps'] if app not in BLACKLIST]
    except Exception as e:
        warnings.warn('Error %s during loading %s' % (e, conf['apps']))

    for app in filtered_apps:
        try:
            app_module = import_module(app)
            if app_module != mod:
                app_module = _get_correct_module(app_module)
                if depth < max_depth:
                    mod_conf = extract_conf_from(app_module, depth=depth+1)
                    for k, v in six.iteritems(mod_conf):
                        # prevent config duplicity
                        # skip config merge
                        if k == 'config':
                            continue
                        if isinstance(v, dict):
                            conf[k].update(v)
                        elif isinstance(v, (list, tuple)):
                            conf[k] = merge(conf[k], v)
        except Exception as e:
            pass  # swallow, but maybe log for info what happens
    return conf


def _get_correct_module(mod):
    """returns imported module
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

    conf = Config(CONF_SPEC)

    # get imported module
    mod = _get_correct_module(mod)

    conf.set_module(mod)

    # extarct from default object or from module
    if hasattr(mod, 'default'):
        default = mod.default
        conf = extract_conf_from(default, conf)
    else:
        conf = extract_conf_from(mod, conf)
    return conf
