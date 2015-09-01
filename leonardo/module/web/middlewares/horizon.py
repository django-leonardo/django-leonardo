
from __future__ import absolute_import

import json
import logging
import time
import six
from django import http
from django.conf import settings
from django.contrib import messages as django_messages
from django.utils import timezone
from horizon.utils import functions as utils

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
