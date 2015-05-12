
import functools
from django.conf import settings
from datetime import datetime, timedelta

CACHE_EXPIRATION = getattr(settings, 'CACHE_EXPIRATION', 3600)


class memoized(object):

    """Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated), unless more than expiration passed. Designed only for
    widget functions.
    """

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        id = "{}-{}-{}".format(args[0]._meta.app_label, args[0].__class__.__name__ , args[0].id)
        expirated = datetime.now() - timedelta(seconds=CACHE_EXPIRATION)
        if id in self.cache \
                and self.cache[id][0] >= expirated:
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
