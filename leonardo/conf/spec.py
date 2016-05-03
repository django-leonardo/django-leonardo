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
    'js_compress_files': [],
    'js_external_files': [],
    'js_files': [],
    'js_spec_files': [],
    'angular_modules': [],
    'css_files': [],
    'scss_files': [],
    'config': {},
    'additional_fields': {},
    'migration_modules': {},
    'absolute_url_overrides': {},
    'navigation_extensions': [],
    'page_actions': [],
    'widget_actions': [],
    'ordering': 0,
    'channel_routing': [],
}

# just MAP - Django - Our spec
DJANGO_CONF = {
    'INSTALLED_APPS': "apps",
    'APPLICATION_CHOICES': "plugins",
    'MIDDLEWARE_CLASSES': "middlewares",
    'AUTHENTICATION_BACKENDS': "auth_backends",
    'PAGE_EXTENSIONS': "page_extensions",
    'ADD_JS_FILES': "js_files",
    'ADD_JS_COMPRESS_FILES': "js_compress_files",
    'PAGE_EXTENSIONS': "page_extensions",
    'ADD_PAGE_ACTIONS': "page_actions",
    'ADD_WIDGET_ACTIONS': "widget_actions",
    'ADD_CSS_FILES': "css_files",
    'ADD_JS_FILES': "js_files",
    'ADD_JS_SPEC_FILES': "js_spec_files",
    'ADD_SCSS_FILES': "scss_files",
    'ADD_ANGULAR_MODULES': "angular_modules",
    'MIGRATION_MODULES': "migration_modules",
    'CONSTANCE_ADDITIONAL_FIELDS': "additional_fields",
}

try:
    from local_settings import LEONARDO_CONF_SPEC
    CONF_SPEC.update(LEONARDO_CONF_SPEC)
except ImportError:
    pass
else:
    # TODO: say something useful
    pass

try:
    from local_settings import LEONARDO_DJANGO_CONF
    DJANGO_CONF.update(LEONARDO_DJANGO_CONF)
except ImportError:
    pass
