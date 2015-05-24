
=======================
Development Environment
=======================

Simplest way is using our SaltStack Formula where you can comfortably specify sources for leonardo with plugins.

usualy without any prerequirements you can do something like this

.. code-block:: bash

    virtualenv -p /usr/bin/python2.7 /srv/leonardo/sites/mysite
    
    git clone https://github.com/django-leonardo/django-leonardo.git -b develop /srv/leonardo/sites/mysite/leonardo

    vim /srv/leonardo/sites/mysite/local_settings.py


put your config to ``local_settings.py``::

    # -*- coding: utf-8 -*-

    from __future__ import absolute_import

    import sys
    from os.path import join, dirname, abspath, normpath

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': '127.0.0.1',
            'NAME': 'leonardo_mysite',
            'PASSWORD': 'mysite_password',
            'USER': 'leonardo_mysite'
        }
    }

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
            'TIMEOUT': 120,
            'KEY_PREFIX': 'CACHE_MYSITE'
        }
    }

    SECRET_KEY = 'my_secret_key'

    DEBUG = True

    MEDIA_ROOT = '/srv/leonardo/sites/mysite/media/'
    STATIC_ROOT = '/srv/leonardo/sites/mysite/static/'

    TIME_ZONE = 'Europe/Prague'

    LANGUAGE_CODE = 'en'

    # your app here
    APPS = [
        'blog',
        'forms',
        'news'
    ]

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'root': {
            'level': 'WARNING',
            'handlers': ['file'],
        },
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'formatters': {
            'verbose': {
                'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                'datefmt' : "%d/%b/%Y %H:%M:%S"
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': '/srv/leonardo/sites/mysite/leonardo_server.log',
                'formatter': 'verbose'
            },
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler',
                'formatter': 'simple',
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins', 'file'],
                'level': 'DEBUG',
                'propagate': True,
            },
        }
    }

Run
---

There are several options which you can use, see contrib directory in the repo https://github.com/django-leonardo/django-leonardo/tree/master/contrib

Django ``runserver``

.. code-block:: bash

    python /srv/leonardo/sites/mysite/leonardo/contrib/django/manage.py runserver 0.0.0.0:80
    
Tornado

.. code-block:: bash

    python /srv/leonardo/sites/mysite/leonardo/contrib/tornado/server

