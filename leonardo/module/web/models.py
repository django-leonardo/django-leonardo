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


@python_2_unicode_compatible
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

    def __str__(self):
        return "{0} - {1}".format(self.page, self.size)

    class Meta:
        verbose_name = _("Page dimension")
        verbose_name_plural = _("Page dimensions")


@python_2_unicode_compatible
class PageTheme(models.Model):

    name = models.CharField(
        verbose_name=_("Name"), max_length=255, null=True, blank=True)
    label = models.CharField(
        verbose_name=_("Title"), max_length=255, null=True, blank=True)
    template = models.ForeignKey(
        'dbtemplates.Template', verbose_name=_('Template'), related_name='page_templates', limit_choices_to={'name__startswith': "base/page/"})
    style = models.TextField(verbose_name=_('Style'), blank=True)

    def __str__(self):
        return self.label or super(PageTheme, self).__str__()

    class Meta:
        verbose_name = _("Page theme")
        verbose_name_plural = _("Page themes")


@python_2_unicode_compatible
class PageColorScheme(models.Model):

    name = models.CharField(
        verbose_name=_("Name"), max_length=255, null=True, blank=True)
    label = models.CharField(
        verbose_name=_("Title"), max_length=255, null=True, blank=True)
    style = models.TextField(verbose_name=_('Style'), blank=True)
    theme = models.ForeignKey(
        PageTheme, verbose_name=_('Template'), related_name='templates')

    def __str__(self):
        return self.label or super(PageColorScheme, self).__str__()

    class Meta:
        verbose_name = _("Page color scheme")
        verbose_name_plural = _("Page color schemes")


class Page(FeinCMSPage):

    theme = models.ForeignKey(PageTheme, verbose_name=_('Theme'))
    color_scheme = models.ForeignKey(PageColorScheme, verbose_name=_('Color scheme'))

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")
        ordering = ['tree_id', 'lft']

    @property
    def dimensions(self):
        return PageDimension.objects.filter(
            page=self)

    def get_col_classes(self, col='col1'):

        STR = "col-{0}-{1}"
        classes = []
        for d in self.dimensions:
            classes.append(
                STR.format(
                    d.size, getattr(d, '{}_width'.format(col))))
        return " ".join(classes)


@python_2_unicode_compatible
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

    @property
    def width_class(self):
        STR = "col-{0}-{1}"
        return STR.format(self.size, self.width)

    def __str__(self):
        return "{0} - {1}".format(self.widget_type, self.width_class)

    class Meta:
        verbose_name = _("Widget dimension")
        verbose_name_plural = _("Widget dimensions")


class WidgetInline(FeinCMSInline):
    form = WidgetForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "base_theme":
            queryset = WidgetBaseTheme.objects.all()
            kwargs["queryset"] = queryset
            kwargs["initial"] = queryset.first()
        if db_field.name == "content_theme":
            queryset = WidgetContentTheme.objects.filter(
                widget_class=self.model.__name__)
            kwargs["queryset"] = queryset
            kwargs["initial"] = queryset.first()
        return super(WidgetInline, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

    def __init__(self, *args, **kwargs):
        super(WidgetInline, self).__init__(*args, **kwargs)

        self.fieldsets = [
            (None, {
                'fields': [
                    list(self.model.fields())
                ],
            }),
            (_('Theme'), {
                'fields': [
                    ('label', 'base_theme', 'content_theme', 'enabled',),
                ],
            }),
        ]


@python_2_unicode_compatible
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

    @property
    def width_class(self):
        STR = "col-{0}-{1}"
        return STR.format(self.size, self.width)

    def __str__(self):
        return "{0} - {1}".format(self.widget_type, self.width_class)

    class Meta:
        verbose_name = _("Widget dimension")
        verbose_name_plural = _("Widget dimensions")


@python_2_unicode_compatible
class WidgetContentTheme(models.Model):

    name = models.CharField(
        verbose_name=_("Name"), max_length=255, null=True, blank=True)
    label = models.CharField(
        verbose_name=_("Title"), max_length=255, null=True, blank=True)
    template = models.ForeignKey(
        'dbtemplates.Template', verbose_name=_('Content template'), related_name='content_templates', limit_choices_to={'name__startswith': "widget/"})
    style = models.TextField(verbose_name=_('Content style'), blank=True)
    widget_class = models.CharField(
        verbose_name=_('Widget class'), max_length=255)

    def __str__(self):
        return self.label or str(self._meta.verbose_name + ' %s' % self.pk)

    class Meta:
        verbose_name = _("Widget content theme")
        verbose_name_plural = _("Widget content themes")


@python_2_unicode_compatible
class WidgetBaseTheme(models.Model):

    name = models.CharField(
        verbose_name=_("Name"), max_length=255, null=True, blank=True)
    label = models.CharField(
        verbose_name=_("Title"), max_length=255, null=True, blank=True)
    template = models.ForeignKey(
        'dbtemplates.Template', verbose_name=_('Base template'), related_name='base_templates', limit_choices_to={'name__startswith': "base/widget/"})

    style = models.TextField(verbose_name=_('Base style'), blank=True)

    def __str__(self):
        return self.label or str(self._meta.verbose_name + ' %s' % self.pk)

    class Meta:
        verbose_name = _("Widget base theme")
        verbose_name_plural = _("Widget base themes")


class Widget(FeinCMSBase):

    feincms_item_editor_inline = WidgetInline

    prerendered_content = models.TextField(
        verbose_name=_('prerendered content'), blank=True, editable=False)
    enabled = models.NullBooleanField(verbose_name=_('Is visible?'))
    label = models.CharField(
        verbose_name=_("Title"), max_length=255, null=True, blank=True)
    base_theme = models.ForeignKey(WidgetBaseTheme, verbose_name=_('Base theme'))
    content_theme = models.ForeignKey(WidgetContentTheme, verbose_name=_('Content theme'))

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
        return self.content_theme.template

    @property
    def get_template(self):
        return self.content_theme.template

    def _template_xml_name(self):
        template = 'default'
        return u'widget/%s/%s.xml' % (self.widget_name, template)
    template_xml_name = property(_template_xml_name)

    @property
    def widget_name(self):
        return self.__class__.__name__.lower().replace('widget', '')

    @property
    def get_base_template(self):
        return self.base_theme.template

    @property
    def widget_label(self):
        return self._meta.verbose_name

    def render(self, **kwargs):
        return self.render_content(kwargs)

    def render_content(self, options):

        base_template = self.base_theme.template
        template = loader.get_template(self.content_theme.template)

        context = RequestContext(options['request'], {
            'widget': self,
            'base_template': self.get_base_template,
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

    @property
    def dimensions(self):
        return WidgetDimension.objects.filter(
            widget_id=self.pk,
            widget_type=ContentType.objects.get_for_model(self))

    @property
    def render_box_classes(self):
        """agreggate all css classes
        """
        classes = []
        for d in self.dimensions:
            classes.append(d.width_class)
        return " ".join(classes)

    @classmethod
    @memoized
    def templates(cls, choices=False, suffix=True):
        """returns widget templates located in ``templates/widget/widgetname``
        """
        widget_name = cls.__name__.lower().replace('widget', '')

        pattern = 'widget/{0}/'.format(widget_name)
        res = find_all_templates('{0}*'.format(pattern))

        if choices:
            return template_choices(res, suffix=suffix)
        return res

    @classmethod
    def fields(cls):
        widget_fields = [
            f.name for f in Widget._meta.fields]

        return fields_for_model(
            cls, exclude=widget_fields,
            widgets=WIDGETS)
