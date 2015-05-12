
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
        try:
            instance = args[0]
            request = args[1]['request']
            id = "{}-{}-{}-{}".format(
                instance._meta.app_label,
                instance.__class__.__name__,
                instance.id,
                request.user)
            expirated = datetime.now() - timedelta(seconds=CACHE_EXPIRATION)
            if id in self.cache \
                    and self.cache[id][0] >= expirated:
                return self.cache[id][1]
            else:
                content = self.func(*args)
                self.cache[id] = datetime.now(), content
                return content
        except Exception:
            # all process is optional if failed nothing to do
            return self.func(*args)

    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__

    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)
