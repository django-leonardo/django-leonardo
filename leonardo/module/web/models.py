# -#- coding: utf-8 -#-

from __future__ import unicode_literals

import os
import sys

from dbtemplates.models import Template
from django import forms
from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.forms.models import fields_for_model
from django.template import loader, RequestContext
from django.template.loader import render_to_string
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields.json import JSONField
from feincms.admin.item_editor import FeinCMSInline, ItemEditorForm
from feincms.models import Base as FeinCMSBase
from feincms.module.page.models import BasePage as FeinCMSPage
from horizon.utils.memoized import memoized
from leonardo.utils.templates import find_all_templates, template_choices

from .const import *
from .forms import WidgetForm, WIDGETS


class PageDimension(models.Model):

    page = models.ForeignKey('Page', verbose_name=_('Page'))
    size = models.CharField(
        verbose_name="Size", max_length=20, choices=DISPLAY_SIZE_CHOICES, default='md')
    col1_width = models.IntegerField(verbose_name=_("Column 1 width"),
                                     choices=COLUMN_CHOICES, default=DEFAULT_WIDTH)
    col2_width = models.IntegerField(verbose_name=_("Column 2 width"),
                                     choices=COLUMN_CHOICES, default=DEFAULT_WIDTH)
    col3_width = models.IntegerField(verbose_name=_("Column 3 width"),
                                     choices=COLUMN_CHOICES, default=DEFAULT_WIDTH)

    class Meta:
        verbose_name = _("Page Dimension")
        verbose_name_plural = _("Page Dimensions")


@python_2_unicode_compatible
class PageTheme(models.Model):

    label = models.CharField(
        verbose_name=_("Title"), max_length=255, null=True, blank=True)
    template = models.ForeignKey(
        'dbtemplates.Template', verbose_name=_('Template'), related_name='templates')

    style = models.TextField(verbose_name=_('Style'), blank=True)

    def __str__(self):
        return self.label or super(PageTheme, self).__str__()

    class Meta:
        verbose_name = _("Page theme")
        verbose_name_plural = _("Page themes")

class Page(FeinCMSPage):

    theme = models.ForeignKey(PageTheme, verbose_name=_('Theme'))

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")
        ordering = ['tree_id', 'lft']


class WidgetInline(FeinCMSInline):
    form = WidgetForm

    def __init__(self, *args, **kwargs):
        super(WidgetInline, self).__init__(*args, **kwargs)
        widget_fields = [f.name for f in Widget._meta.fields if f.name not in [
            'options', 'prerendered_content']]
        self.fieldsets = [
            (None, {
                'fields': [
                    list(self.model.fields())
                ],
            }),
            (_('Theme'), {
                'fields': [
                    ('label', 'theme', ),
                ],
            }),

        ]


class WidgetDimension(models.Model):

    widget_type = models.ForeignKey(ContentType)
    widget_id = models.PositiveIntegerField()
    widget_object = generic.GenericForeignKey('widget_type', 'widget_id')

    size = models.CharField(
        verbose_name="Size", max_length=20, choices=DISPLAY_SIZE_CHOICES, default='md')
    width = models.IntegerField(verbose_name=_("Width"),
                                choices=COLUMN_CHOICES, default=DEFAULT_WIDTH)
    height = models.IntegerField(verbose_name=_("Height"),
                                 choices=ROW_CHOICES, default=DEFAULT_WIDTH)
    offset = models.IntegerField(verbose_name=_("Offset"),
                                 choices=COLUMN_CHOICES, default=DEFAULT_WIDTH)

    class Meta:
        verbose_name = _("Widget Dimension")
        verbose_name_plural = _("Widget Dimensions")


@python_2_unicode_compatible
class WidgetTheme(models.Model):

    label = models.CharField(
        verbose_name=_("Title"), max_length=255, null=True, blank=True)
    content_template = models.ForeignKey(
        'dbtemplates.Template', verbose_name=_('Content template'), related_name='content_templates')
    base_template = models.ForeignKey(
        'dbtemplates.Template', verbose_name=_('Base template'), related_name='base_templates')

    widget_class = models.CharField(
        verbose_name=_('Widget class'), max_length=255)

    style = models.TextField(verbose_name=_('Style'), blank=True)

    def __str__(self):
        return self.label or super(WidgetTheme, self).__str__()

    class Meta:
        verbose_name = _("Widget theme")
        verbose_name_plural = _("Widget themes")


class Widget(FeinCMSBase):

    feincms_item_editor_inline = WidgetInline

    prerendered_content = models.TextField(
        verbose_name=_('prerendered content'), blank=True, editable=False)
    enabled = models.NullBooleanField(verbose_name=_('Is visible?'))
    label = models.CharField(
        verbose_name=_("Title"), max_length=255, null=True, blank=True)
    theme = models.ForeignKey(WidgetTheme, verbose_name=_('Theme'))

    class Meta:
        abstract = True
        verbose_name = _("Abstract widget")
        verbose_name_plural = _("Abstract widgets")

    def __str__(self):
        return self.label or super(Widget, self).__str__()

    def thumb_geom(self):
        return config_value('MEDIA', 'THUMB_MEDIUM_GEOM')

    def thumb_options(self):
        return config_value('MEDIA', 'THUMB_MEDIUM_OPTIONS')

    def get_template_name(self, format='html'):
        return self.theme.content_template

    @property
    def get_template(self):
        return self.theme.content_template

    def _template_xml_name(self):
        template = 'default'
        return u'widget/%s/%s.xml' % (self.widget_name, template)
    template_xml_name = property(_template_xml_name)

    def _widget_name(self):
        return self.__class__.__name__.lower().replace('widget', '')
    widget_name = property(_widget_name)

    def _widget_label(self):
        return self._meta.verbose_name
    widget_label = property(_widget_label)

    def render(self, **kwargs):
        return self.render_content(kwargs)

    def render_content(self, options):

        base_template = self.theme.base_template
        template = loader.get_template(self.theme.content_template)

        context = RequestContext(options['request'], {
            'widget': self,
            'base_template': base_template,
            'request': options['request'],
        })
        return template.render(context)

    def render_error(self, error_code):
        return render_to_string("widget/error.html", {
            'widget': self,
            'request': kwargs['request'],
        })

    def model_cls(self):
        return self.__class__.__name__

    @classmethod
    def fields(cls):
        widget_fields = [
            f.name for f in Widget._meta.fields
            if f.name not in ['options', 'prerendered_content']]

        return fields_for_model(
            cls, exclude=widget_fields,
            widgets=WIDGETS)
