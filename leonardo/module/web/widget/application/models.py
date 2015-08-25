# -#- coding: utf-8 -#-

from __future__ import absolute_import, unicode_literals

from email.utils import parsedate
from time import mktime
from random import SystemRandom
import re

from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import (
    Resolver404, resolve, reverse, NoReverseMatch)
from django.db import models
from django.db.models import signals
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.utils.functional import curry as partial, lazy, wraps
from django.utils.http import http_date
from django.utils.safestring import mark_safe
from django.utils.translation import get_language, ugettext_lazy as _

from feincms.admin.item_editor import ItemEditorForm
from feincms.contrib.fields import JSONField
from feincms.translations import short_language_code
from feincms.utils import get_object



from django.db import models
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.utils.translation import ugettext_lazy as _
from feincms.content.application.models import (ApplicationContent)
from leonardo.module.web.models import Widget
from feincms.admin.item_editor import ItemEditorForm


from leonardo.module.web.widgets.forms import WidgetUpdateForm


class ApplicationWidget(Widget, ApplicationContent):

    @classmethod
    def initialize_type(cls, APPLICATIONS):
        for i in APPLICATIONS:
            if not 2 <= len(i) <= 3:
                raise ValueError(
                    "APPLICATIONS must be provided with tuples containing at"
                    " least two parameters (urls, name) and an optional extra"
                    " config dict")

            urls, name = i[0:2]

            if len(i) == 3:
                app_conf = i[2]

                if not isinstance(app_conf, dict):
                    raise ValueError(
                        "The third parameter of an APPLICATIONS entry must be"
                        " a dict or the name of one!")
            else:
                app_conf = {}

            cls.ALL_APPS_CONFIG[urls] = {
                "urls": urls,
                "name": name,
                "config": app_conf
            }

        cls.add_to_class(
            'urlconf_path',
            models.CharField(_('application'), max_length=100, choices=[
                (c['urls'], c['name']) for c in cls.ALL_APPS_CONFIG.values()])
        )

        class ApplicationContentItemEditorForm(WidgetUpdateForm):
            app_config = {}
            custom_fields = {}

            def __init__(self, *args, **kwargs):
                super(ApplicationContentItemEditorForm, self).__init__(
                    *args, **kwargs)

                instance = kwargs.get("instance", None)

                if instance:
                    try:
                        # TODO use urlconf_path from POST if set
                        # urlconf_path = request.POST.get('...urlconf_path',
                        #     instance.urlconf_path)
                        self.app_config = cls.ALL_APPS_CONFIG[
                            instance.urlconf_path]['config']
                    except KeyError:
                        self.app_config = {}

                    self.custom_fields = {}
                    admin_fields = self.app_config.get('admin_fields', {})

                    if isinstance(admin_fields, dict):
                        self.custom_fields.update(admin_fields)
                    else:
                        get_fields = get_object(admin_fields)
                        self.custom_fields.update(
                            get_fields(self, *args, **kwargs))

                    params = self.instance.parameters
                    for k, v in self.custom_fields.items():
                        v.initial = params.get(k)
                        self.fields[k] = v
                        if k in params:
                            self.fields[k].initial = params[k]

    def render_content(self, options):
        data = {
            'widget': self,
            'request': options.get('request'),
        }
        context = RequestContext(options.get('request'), data)

        context['content'] = getattr(
            self, 'rendered_result', '')

        return render_to_string(self.get_template, context)

    def process(self, request, **kw):
        page_url = self.parent.get_absolute_url()

        if "path_mapper" in self.app_config:
            path_mapper = get_object(self.app_config["path_mapper"])
            path, page_url = path_mapper(
                request.path,
                page_url,
                appcontent_parameters=self.parameters
            )
        else:
            path = request._feincms_extra_context['extra_path']


        # Resolve the module holding the application urls.
        urlconf_path = self.app_config.get('urls', self.urlconf_path)

        try:
            fn, args, kwargs = resolve(path, urlconf_path)
        except (ValueError, Resolver404):
            raise Resolver404(str('Not found (resolving %r in %r failed)') % (
                path, urlconf_path))

        # Variables from the ApplicationContent parameters are added to request
        # so we can expose them to our templates via the appcontent_parameters
        # context_processor
        request._feincms_extra_context.update(self.parameters)
        request._feincms_extra_context.update({'widget': self})

        # Save the application configuration for reuse elsewhere
        request._feincms_extra_context.update({
            'app_config': dict(
                self.app_config,
                urlconf_path=self.urlconf_path,
            ),
        })

        view_wrapper = self.app_config.get("view_wrapper", None)
        if view_wrapper:
            fn = partial(
                get_object(view_wrapper),
                view=fn,
                appcontent_parameters=self.parameters
            )

        output = fn(request, *args, **kwargs)

        if isinstance(output, HttpResponse):
            if self.send_directly(request, output):
                return output
            elif output.status_code == 200:
                output.context_data['widget'] = self

                if self.unpack(request, output) and 'view' in kw:
                    # Handling of @unpack and UnpackTemplateResponse
                    kw['view'].template_name = output.template_name
                    kw['view'].request._feincms_extra_context.update(
                        output.context_data)

                else:
                    # If the response supports deferred rendering, render the
                    # response right now. We do not handle template response
                    # middleware.
                    if hasattr(output, 'render') and callable(output.render):
                        output.render()

                    self.rendered_result = mark_safe(
                        output.content.decode('utf-8'))

                self.rendered_headers = {}

                # Copy relevant headers for later perusal
                for h in ('Cache-Control', 'Last-Modified', 'Expires'):
                    if h in output:
                        self.rendered_headers.setdefault(
                            h, []).append(output[h])

        elif isinstance(output, tuple) and 'view' in kw:
            kw['view'].template_name = output[0]
            kw['view'].request._feincms_extra_context.update(output[1])

        else:
            self.rendered_result = mark_safe(output)

        return True  # successful

    class Meta:
        abstract = True
        verbose_name = _("External application")
        verbose_name_plural = _('External applications')
