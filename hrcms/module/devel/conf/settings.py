
from project.conf.settings import SITE_ID, SITE_NAME

INTERNAL_IPS = (
    '192.168.127.1',
    '192.168.137.1',
    '192.168.1.132',
    '195.113.118.50',
    '77.240.98.212',
    '217.28.92.126',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS' : True,
}

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
#    'debug_toolbar.panels.profiling.ProfilingDebugPanel',
#    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
#    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
#    'debug_toolbar.panels.cache.CacheDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
#    'debug_toolbar.panels.state.StateDebugPanel',
#    'debug_toolbar.panels.htmlvalidator.HTMLValidationDebugPanel',
)

DEBUG = True
ASSETS_DEBUG = DEBUG
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'NAME': 'django12_%s_dev' % SITE_NAME,
        'PASSWORD': 'pass_%s' % SITE_NAME,
        'USER': 'django12_%s_dev' % SITE_NAME
    }
}
