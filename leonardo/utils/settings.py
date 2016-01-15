

import warnings

from django.utils import six
from importlib import import_module
from leonardo.conf.spec import CONF_SPEC
from leonardo.conf.base import ModuleConfig

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


def _is_leonardo_module(whatever):
    '''check if is leonardo module'''

    # check if is python module
    if hasattr(whatever, 'default') \
            or hasattr(whatever, 'leonardo_module_conf'):
        return True

    # check if is python object
    for key in dir(whatever):
        if 'LEONARDO' in key:
            return True


def extract_conf_from(mod, conf=ModuleConfig(CONF_SPEC), depth=0, max_depth=2):
    """recursively extract keys from module or object
    by passed config scheme
    """

    # extract config keys from module or object
    for key, default_value in six.iteritems(conf):
        conf[key] = _get_key_from_module(mod, key, default_value)

    # support for recursive dependecies
    try:
        filtered_apps = [app for app in conf['apps'] if app not in BLACKLIST]
    except TypeError:
        pass
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

    elif hasattr(mod, 'default_app_config'):
        # use django behavior
        mod_path, _, cls_name = mod.default_app_config.rpartition('.')
        _mod = import_module(mod_path)
        config_class = getattr(_mod, cls_name)
        # check if is leonardo config compliant
        if _is_leonardo_module(config_class):
            mod = config_class

    return mod


def get_conf_from_module(mod):
    """return configuration from module with defaults no worry about None type

    """

    conf = ModuleConfig(CONF_SPEC)

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
