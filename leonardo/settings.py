
from __future__ import absolute_import

import os
import six
import logging
import warnings

from django.apps import apps
from django import VERSION
from leonardo.conf.spec import DJANGO_CONF
from leonardo.base import leonardo, default
from leonardo.utils.settings import (get_conf_from_module, merge,
                                     get_loaded_modules)
from importlib import import_module  # noqa
from django.utils.module_loading import module_has_submodule  # noqa


_file_path = os.path.abspath(os.path.dirname(__file__)).split('/')

BASE_DIR = '/'.join(_file_path[0:-2])

from leonardo.conf.default import *

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
STATIC_URL = '/static/'


if VERSION[:2] >= (1, 8):

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)), 'templates')
            ],
            'OPTIONS': {
                'context_processors': default.context_processors,
                'loaders': [
                    'dbtemplates.loader.Loader',
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                    'horizon.loaders.TemplateLoader',
                ],
                'debug': True
            },
        },
    ]

else:

    TEMPLATE_DIRS = [
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'templates')
    ]

    TEMPLATE_CONTEXT_PROCESSORS = default.context_processors

    TEMPLATE_LOADERS = (
        'dbtemplates.loader.Loader',
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'horizon.loaders.TemplateLoader',
    )

try:
    # obsole location since 1.0.3 use `leonrdo_site.settings`
    from leonardo_site.local.settings import *
    warnings.warn(
        'leonardo_site.local.settings is obsolete use new location')
except ImportError:
    pass

try:
    # full settings
    # TODO support configurable from local_settings
    # LEONARDO_PROJECT_NAME = 'leonardo_site'
    from leonardo_site.settings import *
except ImportError:
    pass

try:
    # local settings
    from local_settings import *
except ImportError:
    warnings.warn(
        'local_settings was not found in $PYTHONPATH !')

if not DEBUG:
    if VERSION[:2] >= (1, 8):
        TEMPLATES[0]['OPTIONS']['loaders'] = [
            ('django.template.loaders.cached.Loader', [
                'dbtemplates.loader.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'horizon.loaders.TemplateLoader',
            ])]
        TEMPLATES[0]['OPTIONS']['debug'] = False
else:
    TEMPLATE_DEBUG = DEBUG

APPS = merge(APPS, default.core)

if 'media' in APPS:
    FILER_IMAGE_MODEL = 'leonardo.module.media.models.Image'

try:
    from leonardo.conf.horizon import *
    from leonardo.conf.static import *
except Exception as e:
    warnings.warn(
        'Could not import static packages %s' % str(e))

if LEONARDO_SYSTEM_MODULE:
    APPS = merge(APPS, ['leonardo_system'])
    HORIZON_CONFIG['system_module'] = True
else:
    HORIZON_CONFIG['system_module'] = False

if not apps.ready:
    # load directly specified apps
    leonardo.get_app_modules(APPS)

    # propagate settings to leonardo
    leonardo.MODULES_AUTOLOAD = LEONARDO_MODULE_AUTO_INCLUDE

    # load all modules
    leonardo.load_modules()

    # just propagate all loaded modules to settings
    LEONARDO_MODULES = leonardo.get_modules()

    # iterate over sorted modules
    for mod, mod_cfg in LEONARDO_MODULES:

        try:

            # import all settings keys from module
            if module_has_submodule(mod, "settings"):
                try:
                    settings_mod = import_module(
                        '{0}.settings'.format(mod.__name__))
                    for k in dir(settings_mod):
                        if not k.startswith("_"):
                            val = getattr(settings_mod, k, None)
                            globals()[k] = val
                            locals()[k] = val
                except Exception as e:
                    warnings.warn(
                        'Exception "{}" raised during loading '
                        'settings from {}'.format(str(e), mod))

            # go through django keys and merge it to main settings
            for key in DJANGO_CONF.keys():
                updated_value = mod_cfg.get_value(key, globals()[key])
                globals()[key] = updated_value
                locals()[key] = updated_value
                # map value to leonardo but under our internal name
                setattr(leonardo, DJANGO_CONF[key], updated_value)

            if mod_cfg.urls_conf:
                MODULE_URLS[mod_cfg.urls_conf] = {'is_public': mod_cfg.public}
            # TODO move to utils.settings
            # support for one level nested in config dictionary
            for config_key, config_value in six.iteritems(mod_cfg.config):

                if isinstance(config_value, dict):
                    CONSTANCE_CONFIG_GROUPS.update({config_key: config_value})
                    for c_key, c_value in six.iteritems(config_value):
                        mod_cfg.config[c_key] = c_value
                    # remove from main dict
                    mod_cfg.config.pop(config_key)
                else:
                    if isinstance(mod_cfg.optgroup, six.string_types):
                        CONSTANCE_CONFIG_GROUPS.update({
                            mod_cfg.optgroup: mod_cfg.config})
                    else:
                        if 'ungrouped' in CONSTANCE_CONFIG_GROUPS:
                            CONSTANCE_CONFIG_GROUPS[
                                'ungrouped'].update(mod_cfg.config)
                        else:
                            CONSTANCE_CONFIG_GROUPS['ungrouped'] = \
                                mod_cfg.config

            # import and update absolute overrides
            for model, method in six.iteritems(mod_cfg.absolute_url_overrides):
                try:
                    _mod = import_module(".".join(method.split('.')[:-1]))
                    ABSOLUTE_URL_OVERRIDES[model] = getattr(
                        _mod, method.split('.')[-1])
                except Exception as e:
                    raise e

            for nav_extension in mod_cfg.navigation_extensions:
                try:
                    import_module(nav_extension)
                except ImportError:
                    pass

            CONSTANCE_CONFIG.update(mod_cfg.config)

            if VERSION[:2] >= (1, 8):
                TEMPLATES[0]['DIRS'] = merge(
                    TEMPLATES[0]['DIRS'], mod_cfg.dirs)
                cp = TEMPLATES[0]['OPTIONS']['context_processors']
                TEMPLATES[0]['OPTIONS']['context_processors'] = merge(
                    cp, mod_cfg.context_processors)

            else:

                TEMPLATE_CONTEXT_PROCESSORS = merge(
                    TEMPLATE_CONTEXT_PROCESSORS, mod_cfg.context_processors)
                TEMPLATE_DIRS = merge(TEMPLATE_DIRS, mod_cfg.dirs)

            # collect grouped widgets
            if isinstance(mod_cfg.optgroup, six.string_types):
                if len(mod_cfg.widgets) > 0:
                    WIDGETS[mod_cfg.optgroup] = merge(
                        getattr(WIDGETS, mod_cfg.optgroup, []), mod_cfg.widgets)
            else:
                if len(mod_cfg.widgets) > 0 and DEBUG:
                    warnings.warn('You have ungrouped widgets'
                                  ', please specify your ``optgroup``'
                                  'which categorize your widgets in %s' % mod)
                if len(mod_cfg.widgets) > 0:
                    WIDGETS['ungrouped'] = merge(
                        getattr(WIDGETS, 'ungrouped', []), mod_cfg.widgets)

        except Exception as e:
            warnings.warn(
                'Exception "{}" raised during loading '
                'module {}'.format(str(e), mod))
else:
    warnings.warn("Leonardo modules are already loaded. Skiped now.")

setattr(leonardo, 'widgets', WIDGETS)

# FINALLY OVERRIDE ALL

try:
    # local settings
    from local_settings import *
except ImportError:
    warnings.warn(
        'Missing local_settings !')

try:
    # full settings
    from leonardo_site.local.settings import *
except ImportError:
    pass

try:
    # full settings
    from leonardo_site.settings import *
except ImportError:
    pass

# and again merge core with others
APPS = merge(APPS, default.core)

# go through django keys and merge it to main settings
for key in DJANGO_CONF.keys():
    # map value to leonardo but under our internal name
    setattr(leonardo, DJANGO_CONF[key], globals()[key])

if DEBUG:

    try:
        import debug_toolbar
        INSTALLED_APPS = merge(INSTALLED_APPS, ['debug_toolbar'])
        from leonardo.conf.debug import *
    except ImportError:
        if DEBUG:
            warnings.warn('DEBUG is set to True but, DEBUG tools '
                          'is not installed please run '
                          '"pip install django-leonardo[debug]"')

# async messages
try:
    import async_messages
    INSTALLED_APPS = merge(INSTALLED_APPS, ['async_messages'])
    MIDDLEWARE_CLASSES = merge(MIDDLEWARE_CLASSES,
                               ['async_messages.middleware.AsyncMiddleware'])
except ImportError:
    pass

# use js files instead of horizon
HORIZON_CONFIG['js_files'] = leonardo.js_files
HORIZON_CONFIG['js_compress_files'] = leonardo.js_compress_files
HORIZON_CONFIG['js_spec_files'] = leonardo.js_spec_files
HORIZON_CONFIG['css_files'] = leonardo.css_files
HORIZON_CONFIG['scss_files'] = leonardo.scss_files
HORIZON_CONFIG['angular_modules'] = leonardo.angular_modules
HORIZON_CONFIG['page_actions'] = leonardo.page_actions
HORIZON_CONFIG['widget_actions'] = leonardo.widget_actions
# path horizon config
from horizon import conf
conf.HORIZON_CONFIG = HORIZON_CONFIG

if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
