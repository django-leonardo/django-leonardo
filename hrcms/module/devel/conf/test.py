
from project.conf.settings import SITE_NAME

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'NAME': 'django12_%s_test' % SITE_NAME,
        'PASSWORD': 'pass_%s' % SITE_NAME,
        'USER': 'django12_%s_test' % SITE_NAME
    }
}
