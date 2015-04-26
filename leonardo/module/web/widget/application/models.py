# -#- coding: utf-8 -#-

from django.db import models
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from feincms.content.application.models import (ApplicationContent)
from leonardo.module.web.models import Widget
from feincms.admin.item_editor import ItemEditorForm


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

        class ApplicationContentItemEditorForm(ItemEditorForm):
            app_config = {}
            custom_fields = {}

            def __init__(self, *args, **kwargs):
                request = kwargs.pop('request', None)
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

        try:
            data = {
                'widget': self,
                'content': self.rendered_result
            }
        except:
            data = {
                'widget': self,
                'content': '<div class="alert">no rendered result</div>'
            }
        context = RequestContext(options.get('request'), data)

        return render_to_string(self.get_template, context)

    class Meta:
        abstract = True
        verbose_name = _("external application")
        verbose_name_plural = _('external applications')
