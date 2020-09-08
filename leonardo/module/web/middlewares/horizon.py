
from __future__ import absolute_import

import json
import logging
import time

import six
from django import http, shortcuts
from django.conf import settings
from django.contrib import messages as django_messages
from django.contrib.auth import REDIRECT_FIELD_NAME  # noqa
from django.contrib.auth.views import redirect_to_login  # noqa
from django.utils import timezone
from django.utils.encoding import iri_to_uri  # noqa
from django.utils.translation import ugettext_lazy as _
from horizon.utils import functions as utils
from django.utils.http import is_safe_url
from leonardo import exceptions
from leonardo import messages


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
                # if response['location'].startswith(settings.LOGOUT_URL):
                #     redirect_response = http.HttpResponse(status=401)
                #     # This header is used for handling the logout in JS
                #     redirect_response['logout'] = True
                #     if self.logout_reason is not None:
                #         utils.add_logout_reason(
                #             request, redirect_response, self.logout_reason)
                # else:
                redirect_response = http.HttpResponse()
                # Use a set while checking if we want a cookie's attributes
                # copied
                cookie_keys = set(('max_age', 'expires', 'path', 'domain',
                                   'secure', 'httponly', 'logout_reason'))
                # Copy cookies from HttpResponseRedirect towards HttpResponse
                for cookie_name, cookie in six.iteritems(response.cookies):
                    cookie_kwargs = dict((
                        (key, value) for key, value in six.iteritems(cookie)
                        if key in cookie_keys and value
                    ))
                    redirect_response.set_cookie(
                        cookie_name, cookie.value, **cookie_kwargs)
                redirect_response['X-Horizon-Location'] = response['location']
                upload_url_key = 'X-File-Upload-URL'
                if upload_url_key in response:
                    self.copy_headers(response, redirect_response,
                                      (upload_url_key, 'X-Auth-Token'))
                return redirect_response
            if queued_msgs:
                # TODO(gabriel): When we have an async connection to the
                # client (e.g. websockets) this should be pushed to the
                # socket queue rather than being sent via a header.
                # The header method has notable drawbacks (length limits,
                # etc.) and is not meant as a long-term solution.
                response['X-Horizon-Messages'] = json.dumps(queued_msgs)
        return response

    def process_exception(self, request, exception):
        """Catches internal Horizon exception classes such as NotAuthorized,
        NotFound and Http302 and handles them gracefully.
        """

        if isinstance(exception, (exceptions.NotAuthorized,
                                  exceptions.NotAuthenticated)):
            auth_url = settings.LOGIN_URL
            next_url = None
            # prevent submiting forms after login and
            # use http referer
            if request.method in ("POST", "PUT"):

                referrer = request.META.get('HTTP_REFERER')

                if referrer and is_safe_url(referrer, request.get_host()):
                    next_url = referrer

            if not next_url:
                next_url = iri_to_uri(request.get_full_path())

            if next_url != auth_url:
                field_name = REDIRECT_FIELD_NAME
            else:
                field_name = None

            login_url = request.build_absolute_uri(auth_url)
            response = redirect_to_login(next_url, login_url=login_url,
                                         redirect_field_name=field_name)
            if isinstance(exception, exceptions.NotAuthorized):
                logout_reason = _("Unauthorized. Please try logging in again.")
                utils.add_logout_reason(request, response, logout_reason)
                # delete messages, created in get_data() method
                # since we are going to redirect user to the login page
                response.delete_cookie('messages')

            if request.is_ajax():
                response_401 = http.HttpResponse(status=401)
                response_401['X-Horizon-Location'] = response['location']
                return response_401

            return response

        # If an internal "NotFound" error gets this far, return a real 404.
        if isinstance(exception, exceptions.NotFound):
            raise http.Http404(exception)

        if isinstance(exception, exceptions.Http302):
            # TODO(gabriel): Find a way to display an appropriate message to
            # the user *on* the login form...
            return shortcuts.redirect(exception.location)
