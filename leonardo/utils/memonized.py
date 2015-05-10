
import collections
import functools
from datetime import datetime, timedelta

expiration = 120


class memoyield(object):

    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated), unless more than 5 seconds passed. Designed for yielding
    functions. This does the conversion from a generator to a list and back to
    a generator, so might not be the fastest solution ever.
    '''

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if args in self.cache and self.cache[args][0] >= datetime.now() - timedelta(seconds=expiration):
            for i in self.cache[args][1]:
                yield i
        else:
            gen = self.func(*args)
            value = list(gen)
            self.cache[args] = datetime.now(), value
            for i in value:
                yield i

    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__

    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)