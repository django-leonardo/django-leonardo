# -*- coding: UTF-8 -*-
import datetime
import json
import logging
import os
import time
from datetime import datetime, timedelta

import six
from django import http, shortcuts
from django.conf import settings
from django.contrib import messages as django_messages
from django.contrib import auth
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.contrib.sites.models import Site
from django.core import exceptions, urlresolvers
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import loading
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.encoding import iri_to_uri
from django.utils.translation import ugettext as __
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import activate
from feincms.content.application.models import reverse
from feincms.module.page.models import Page
from horizon import exceptions, messages
from horizon.utils import functions as utils
from hrcms.module.web.models import build_options
from livesettings import config_value

LOG = logging.getLogger(__name__)


class HorizonMiddleware(object):
    """The main Horizon middleware class. Required for use of Horizon."""

    logout_reason = None

    def process_request(self, request):
        """Adds data necessary for Horizon to function to the request."""
        # Activate timezone handling
        tz = request.session.get('django_timezone')
        if tz:
            timezone.activate(tz)

        # Check for session timeout
        try:
            timeout = settings.SESSION_TIMEOUT
        except AttributeError:
            timeout = 1800

        last_activity = request.session.get('last_activity', None)
        timestamp = int(time.time())
        request.horizon = {'dashboard': None,
                           'panel': None,
                           'async_messages': []}

        if not hasattr(request, "user") or not request.user.is_authenticated():
            # proceed no further if the current request is already known
            # not to be authenticated
            return None
        if request.is_ajax():
            # if the request is Ajax we do not want to proceed, as clients can
            #  1) create pages with constant polling, which can create race
            #     conditions when a page navigation occurs
            #  2) might leave a user seemingly left logged in forever
            #  3) thrashes db backed session engines with tons of changes
            return None
        # If we use cookie-based sessions, check that the cookie size does not
        # reach the max size accepted by common web browsers.
        if (
            settings.SESSION_ENGINE ==
            'django.contrib.sessions.backends.signed_cookies'
        ):
            max_cookie_size = getattr(
                settings, 'SESSION_COOKIE_MAX_SIZE', None)
            session_cookie_name = getattr(
                settings, 'SESSION_COOKIE_NAME', None)
            session_key = request.COOKIES.get(session_cookie_name)
            if max_cookie_size is not None and session_key is not None:
                cookie_size = sum((
                    len(key) + len(value)
                    for key, value in six.iteritems(request.COOKIES)
                ))
                if cookie_size >= max_cookie_size:
                    LOG.error(
                        'Total Cookie size for user_id: %(user_id)s is '
                        '%(cookie_size)sB >= %(max_cookie_size)sB. '
                        'You need to configure file-based or database-backed '
                        'sessions instead of cookie-based sessions: '
                        'http://docs.openstack.org/developer/horizon/topics/'
                        'deployment.html#session-storage'
                        % {
                            'user_id': request.session.get(
                                'user_id', 'Unknown'),
                            'cookie_size': cookie_size,
                            'max_cookie_size': max_cookie_size,
                        }
                    )

        request.session['last_activity'] = timestamp

    def process_response(self, request, response):
        """Convert HttpResponseRedirect to HttpResponse if request is via ajax
        to allow ajax request to redirect url
        """

        if request.is_ajax() and hasattr(request, 'horizon'):
            queued_msgs = request.horizon['async_messages']
            if type(response) == http.HttpResponseRedirect:
                # Drop our messages back into the session as per usual so they
                # don't disappear during the redirect. Not that we explicitly
                # use django's messages methods here.
                for tag, message, extra_tags in queued_msgs:
                    getattr(django_messages, tag)(request, message, extra_tags)
                if response['location'].startswith(settings.LOGOUT_URL):
                    redirect_response = http.HttpResponse(status=401)
                    # This header is used for handling the logout in JS
                    redirect_response['logout'] = True
                    if self.logout_reason is not None:
                        utils.add_logout_reason(
                            request, redirect_response, self.logout_reason)
                else:
                    redirect_response = http.HttpResponse()
                # Copy cookies from HttpResponseRedirect towards HttpResponse
                for cookie_name, cookie in six.iteritems(response.cookies):
                    cookie_kwargs = dict((
                        (key, value) for key, value in six.iteritems(cookie)
                        if key in ('max_age', 'expires', 'path', 'domain',
                            'secure', 'httponly', 'logout_reason') and value
                    ))
                    redirect_response.set_cookie(
                        cookie_name, cookie.value, **cookie_kwargs)
                redirect_response['X-Horizon-Location'] = response['location']
                return redirect_response
            if queued_msgs:
                # TODO(gabriel): When we have an async connection to the
                # client (e.g. websockets) this should be pushed to the
                # socket queue rather than being sent via a header.
                # The header method has notable drawbacks (length limits,
                # etc.) and is not meant as a long-term solution.
                response['X-Horizon-Messages'] = json.dumps(queued_msgs)
        return response


class WebcmsMiddleware(object):
    """old webcms middleware

    added some extra to request and page

    """
    def process_request(self, request):
        try:
            webcms_options = {
                'meta_description': config_value('WEB', 'META_KEYWORDS'),
                'meta_keywords': config_value('WEB', 'META_DESCRIPTION'),
                'meta_title': config_value('WEB', 'META_TITLE'),
            }
            is_private = config_value('WEB', 'IS_PRIVATE')
        except:
            webcms_options = {
                'meta_description': '',
                'meta_keywords': '',
                'meta_title': '',
            }
            is_private = False

        webcms_options['site'] = {
            'name': settings.SITE_NAME,
            'id': settings.SITE_ID,
            'domain': settings.SITE_DOMAIN,
        }

        try:
            page = Page.objects.best_match_for_path(request.path, raise404=True)
            page.options = build_options(page)
            webcms_options['template'] = page.options['template']
            #webcms_options['theme'] = page.options['theme']
            cls_list = []
            for cls in page._feincms_content_types:
                cls_list.append({
                    'name': cls.__name__,
                    'label': cls._meta.verbose_name
                })
            webcms_options['widgets'] = cls_list
        except Exception, e:
            raise e
            page = None
            webcms_options['template'] = 'default'
            webcms_options['theme'] = 'light'
            webcms_options['assets'] = False
            webcms_options['widgets'] = False

        webcms_options['is_private'] = is_private
        request.webcms_page = page
        request.webcms_options = webcms_options
