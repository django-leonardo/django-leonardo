
from __future__ import absolute_import

import functools
from django.conf import settings
from datetime import datetime, timedelta

CACHE_EXPIRATION = getattr(settings, 'CACHE_EXPIRATION', 3600)
LEONARDO_MEMOIZED = getattr(settings, 'LEONARDO_MEMOIZED', True)


class memoized(object):

    """Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated), unless more than expiration passed.
    """

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def is_actual(self, id):
        expirated = datetime.now() - timedelta(seconds=CACHE_EXPIRATION)
        if id in self.cache \
                and self.cache[id][0] >= expirated:
            return True
        return False

    def __call__(self, *args):
        if not LEONARDO_MEMOIZED:
            return self.func(*args)
        instance = args[0]
        id = "{}-{}-{}".format(
            instance._meta.app_label,
            instance.__class__.__name__,
            instance.id)
        if self.is_actual(id):
            return self.cache[id][1]
        else:
            content = self.func(*args)
            self.cache[id] = datetime.now(), content
            return content

    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__

    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)


class page_memoized(memoized):

    """Page specific
    """

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if not LEONARDO_MEMOIZED:
            return self.func(*args)
        instance = args[0]
        id = "{}-{}-{}-{}".format(
            instance._meta.app_label,
            instance.__class__.__name__,
            instance.id,
            args[1])
        if self.is_actual(id):
            return self.cache[id][1]
        else:
            content = self.func(*args)
            self.cache[id] = datetime.now(), content
            return content


class widget_memoized(memoized):

    """Designed only for widget render function.
    """

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):

        if not LEONARDO_MEMOIZED:
            return self.func(*args)

        try:
            instance = args[0]
            request = args[1]['request']
            id = "{}-{}-{}-{}".format(
                instance._meta.app_label,
                instance.__class__.__name__,
                instance.id,
                request.user)
            if self.is_actual():
                return self.cache[id][1]
            else:
                content = self.func(*args)
                self.cache[id] = datetime.now(), content
                return content
        except Exception:
            # all process is optional if failed nothing to do
            return self.func(*args)
