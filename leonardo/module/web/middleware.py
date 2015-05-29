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
from .models import Page, PageColorScheme, PageTheme
from horizon import exceptions, messages
from horizon import conf

from horizon_contrib.common import get_class


def create_new_site():

    """returns page with some widgets
    """

    try:
        theme = PageTheme.objects.first()
    except Exception:
        raise Exception("You havent any themes \
            please install someone and run sync_all")
        theme = None

    page, created = Page.objects.get_or_create(**{
        'title': 'Quickstart',
        'slug': 'quickstart',
        'override_url': '/',
        'featured': False,
        'theme': theme,
        'color_scheme': PageColorScheme.objects.first(),
    })

    return page


class WebMiddleware(object):

    """add extra context to request

    added some extra to request and page

    .. code-block:: python

        request.leonardo_options

        request.LEONARDO_CONFIG

        request.leonardo_page

    supports this syntax

    .. code-block:: python

        request.LEONARDO_CONFIG.DISQUS_COMMENTS

    note: for support old ``webcms`` stuff adds some
    extra stuff which would be old after migration

    """

    def process_response(self, request, response):

        if response.status_code == 404 and Page.objects.count() == 0:

            page = create_new_site()

            return HttpResponseRedirect(reverse('page_update',
                                                kwargs={'page_id': page.pk}))

        if hasattr(request, 'user') and not request.user.is_authenticated():
            response.delete_cookie('frontend_editing')
            request.frontend_editing = False
        return response

    def process_request(self, request):
        try:
            leonardo_options = {
                'meta_description': settings.META_DESCRIPTION,
                'meta_keywords': settings.META_KEYWORDS,
                'meta_title': settings.META_TITLE,
            }
        except:
            leonardo_options = {
                'meta_description': '',
                'meta_keywords': '',
                'meta_title': '',
            }

        leonardo_options['site'] = {
            'name': settings.SITE_NAME,
            'id': settings.SITE_ID,
            'domain': getattr(
                settings, 'SITE_DOMAIN', settings.SITE_NAME + '.cz'),
        }

        try:
            page = Page.objects.best_match_for_path(
                request.path)
        except Exception:
            page = None
            leonardo_options['template'] = 'base.html'
            leonardo_options['theme'] = 'light'
            leonardo_options['assets'] = []
            leonardo_options['widgets'] = []

        request.leonardo_options = leonardo_options
        request.leonardo_page = page

        request.frontend_editing = request.COOKIES.get(
            'frontend_editing', False)

        request.LEONARDO_CONFIG = conf.HORIZON_CONFIG

        # old
        request.webcms_page = page
        request.webcms_options = leonardo_options
