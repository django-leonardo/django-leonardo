"""
Third-party application inclusion support.
"""

from __future__ import absolute_import, unicode_literals

import functools
import re
import warnings
from random import SystemRandom
from threading import local
from time import mktime

import six
from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import *
from django.template.response import TemplateResponse

from .models import ApplicationWidget

APP_REVERSE_CACHE_GENERATION_KEY = 'FEINCMS:APPREVERSECACHE'
APP_REVERSE_CACHE_TIMEOUT = 300


class UnpackTemplateResponse(TemplateResponse):

    """
    Completely the same as marking applicationcontent-contained views with
    the ``feincms.views.decorators.unpack`` decorator.
    """
    _feincms_unpack = True


def cycle_app_reverse_cache(*args, **kwargs):
    """Does not really empty the cache; instead it adds a random element to the
    cache key generation which guarantees that the cache does not yet contain
    values for all newly generated keys"""
    value = '%07x' % (SystemRandom().randint(0, 0x10000000))
    cache.set(APP_REVERSE_CACHE_GENERATION_KEY, value)
    return value


# Set the app_reverse_cache_generation value once per startup (at least).
# This protects us against offline modifications of the database.
cycle_app_reverse_cache()


def app_reverse(viewname, urlconf=None, args=None, kwargs=None, prefix=None,
                *vargs, **vkwargs):
    """
    Reverse URLs from application contents
    Works almost like Django's own reverse() method except that it resolves
    URLs from application contents. The second argument, ``urlconf``, has to
    correspond to the URLconf parameter passed in the ``APPLICATIONS`` list
    to ``Page.create_content_type``::
        app_reverse('mymodel-detail', 'myapp.urls', args=...)
        or
        app_reverse('mymodel-detail', 'myapp.urls', kwargs=...)
    The second argument may also be a request object if you want to reverse
    an URL belonging to the current application content.
    """

    # First parameter might be a request instead of an urlconf path, so
    # we'll try to be helpful and extract the current urlconf from it
    extra_context = getattr(urlconf, '_feincms_extra_context', {})
    appconfig = extra_context.get('app_config', {})
    urlconf = appconfig.get('urlconf_path', urlconf)
    appcontent_class = ApplicationWidget._feincms_content_models[0]
    cache_key = appcontent_class.app_reverse_cache_key(urlconf)
    url_prefix = cache.get(cache_key)

    if url_prefix is None:
        content = appcontent_class.closest_match(urlconf)

        if content is not None:
            if urlconf in appcontent_class.ALL_APPS_CONFIG:
                # We have an overridden URLconf
                app_config = appcontent_class.ALL_APPS_CONFIG[urlconf]
                urlconf = app_config['config'].get('urls', urlconf)

            prefix = content.parent.get_absolute_url()
            prefix += '/' if prefix[-1] != '/' else ''

            url_prefix = (urlconf, prefix)
            cache.set(cache_key, url_prefix, timeout=APP_REVERSE_CACHE_TIMEOUT)

    if url_prefix:
        # vargs and vkwargs are used to send through additional parameters
        # which are uninteresting to us (such as current_app)
        return reverse(
            viewname,
            url_prefix[0],
            args=args,
            kwargs=kwargs,
            prefix=url_prefix[1],
            *vargs, **vkwargs)

    raise NoReverseMatch("Unable to find ApplicationContent for %r" % urlconf)


#: Lazy version of ``app_reverse``
app_reverse_lazy = lazy(app_reverse, str)


def permalink(func):
    """
    Decorator that calls app_reverse()
    Use this instead of standard django.db.models.permalink if you want to
    integrate the model through ApplicationContent. The wrapped function
    must return 4 instead of 3 arguments::
        class MyModel(models.Model):
            @appmodels.permalink
            def get_absolute_url(self):
                return ('myapp.urls', 'model_detail', (), {'slug': self.slug})
    """
    def inner(*args, **kwargs):
        return app_reverse(*func(*args, **kwargs))
    return wraps(func)(inner)


def reverse(viewname, urlconf=None, args=None, kwargs=None, prefix=None, current_app=None):
    """monkey patched reverse

    path supports easy patching 3rd party urls
    if 3rd party app has namespace for example ``catalogue`` and
    you create FeinCMS plugin with same name as this namespace reverse
    returns url from ApplicationContent !

    """

    if not urlconf:
        urlconf = get_urlconf()
    resolver = get_resolver(urlconf)
    args = args or []
    kwargs = kwargs or {}

    if prefix is None:
        prefix = get_script_prefix()

    if not isinstance(viewname, six.string_types):
        view = viewname
    else:
        parts = viewname.split(':')
        parts.reverse()
        view = parts[0]
        path = parts[1:]

        resolved_path = []
        ns_pattern = ''
        while path:
            ns = path.pop()

            # Lookup the name to see if it could be an app identifier
            try:
                app_list = resolver.app_dict[ns]
                # Yes! Path part matches an app in the current Resolver
                if current_app and current_app in app_list:
                    # If we are reversing for a particular app,
                    # use that namespace
                    ns = current_app
                elif ns not in app_list:
                    # The name isn't shared by one of the instances
                    # (i.e., the default) so just pick the first instance
                    # as the default.
                    ns = app_list[0]
            except KeyError:
                pass

            try:
                extra, resolver = resolver.namespace_dict[ns]
                resolved_path.append(ns)
                ns_pattern = ns_pattern + extra
            except KeyError as key:
                for urlconf, config in six.iteritems(
                        ApplicationWidget._feincms_content_models[0].ALL_APPS_CONFIG):
                    partials = viewname.split(':')[1:]

                    try:
                        url = app_reverse(
                            ':'.join(partials), urlconf, args=args, kwargs=kwargs,
                            current_app=current_app, prefix=prefix)
                    except NoReverseMatch:
                        pass
                    else:
                        # ensure that viewname is in urlconf
                        if urlconf.split(".")[-1] in viewname:
                            return url

                if resolved_path:
                    raise NoReverseMatch(
                        "%s is not a registered namespace inside '%s'" %
                        (key, ':'.join(resolved_path)))
                else:
                    raise NoReverseMatch("%s is not a registered namespace" %
                                         key)
        if ns_pattern:
            resolver = get_ns_resolver(ns_pattern, resolver)

    return iri_to_uri(resolver._reverse_with_prefix(view, prefix, *args, **kwargs))


reverse_lazy = lazy(reverse, six.text_type)
