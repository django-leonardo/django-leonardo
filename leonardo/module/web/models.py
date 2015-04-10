# -#- coding: utf-8 -#-

import os
import sys

from django import forms
from django.conf import settings
from django.db import models
from django.forms.models import fields_for_model
from django.template import loader, RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields.json import JSONField
from feincms.admin.item_editor import FeinCMSInline, ItemEditorForm
from feincms.models import Base as FeinCMSBase
from feincms.module.page.models import BasePage as FeinCMSPage
from horizon.utils.memoized import memoized
from leonardo.utils.templates import find_all_templates, template_choices

from .const import *
from .forms import WidgetForm, WIDGETS


class Page(FeinCMSPage):

    col1_width = models.IntegerField(verbose_name=_("Column 1 width"),
                                     choices=COLUMN_CHOICES, default=DEFAULT_WIDTH)
    col2_width = models.IntegerField(verbose_name=_("Column 2 width"),
                                     choices=COLUMN_CHOICES, default=DEFAULT_WIDTH)
    col3_width = models.IntegerField(verbose_name=_("Column 3 width"),
                                     choices=COLUMN_CHOICES, default=DEFAULT_WIDTH)
    col4_width = models.IntegerField(verbose_name=_("Column 4 width"),
                                     choices=COLUMN_CHOICES, default=DEFAULT_WIDTH)
    template_name = models.CharField(
        verbose_name="Template", max_length=255,
        help_text=_("Core HTML templates and CSS styles."), null=True, blank=True)
    theme = models.CharField(verbose_name=_("Theme"), max_length=255, null=True, blank=True,
                             help_text=_("Color and style extension to the template."))

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")
        ordering = ['tree_id', 'lft']


class WidgetInline(FeinCMSInline):
    form = WidgetForm

    def __init__(self, *args, **kwargs):
        super(WidgetInline, self).__init__(*args, **kwargs)
        widget_fields = [f.name for f in Widget._meta.fields if f.name not in ['options', 'prerendered_content'] ]
        self.fieldsets = [
            (None, {
                'fields': [
                    list(self.model.fields())
                ],
            }),
            (_('Theme'), {
                'fields': [
                    ('template_name', 'style', 'border', 'clear'),
                ],
            }),
            (_('Layout'), {
                'fields': [
                    ('pull', 'align', 'push', 'pull'),
                ],
            }),
            (_('Position'), {
                'fields': [
                    ('prepend', 'append', 'vertical_span'),
                ],
            }),
            (_('Visibility'), {
                'fields': [
                    ('visible', 'last'),
                ],
            }),

        ]


class Widget(FeinCMSBase):

    feincms_item_editor_inline = WidgetInline

    options = JSONField(
        verbose_name=_('widget options'), blank=True, editable=False)
    prerendered_content = models.TextField(
        _('prerendered content'), blank=True, editable=False)

    label = models.CharField(
        verbose_name=_("Title"), max_length=255, null=True, blank=True)
    template_name = models.CharField(
        verbose_name=_("Display"), max_length=255, default='default.html')

    span = models.IntegerField(verbose_name=_("Span"),
                               choices=COLUMN_CHOICES, default=DEFAULT_WIDTH)
    vertical_span = models.IntegerField(verbose_name=_("V. Span"),
                                        choices=ROW_CHOICES, default=DEFAULT_WIDTH)
    align = models.IntegerField(
        verbose_name=_("Alignment"), choices=ALIGN_CHOICES, default=DEFAULT_CHOICE)
    vertical_align = models.IntegerField(
        verbose_name=_("V. Alignment"), choices=VERTICAL_ALIGN_CHOICES, default=DEFAULT_CHOICE)
    prepend = models.IntegerField(verbose_name=_("Prepend"),
                                  choices=COLUMN_CHOICES, default=DEFAULT_WIDTH)
    append = models.IntegerField(verbose_name=_("Append"),
                                 choices=COLUMN_CHOICES, default=DEFAULT_CHOICE)
    push = models.IntegerField(verbose_name=_("Push"),
                               choices=COLUMN_CHOICES, default=DEFAULT_CHOICE)
    pull = models.IntegerField(verbose_name=_("Pull"),
                               choices=COLUMN_CHOICES, default=DEFAULT_WIDTH)
    vertical_prepend = models.IntegerField(
        verbose_name=_("V. Prepend"), choices=ROW_CHOICES, default=DEFAULT_CHOICE)
    vertical_append = models.IntegerField(
        verbose_name=_("V. Append"), choices=ROW_CHOICES, default=DEFAULT_CHOICE)
    vertical_push = models.IntegerField(
        verbose_name=_("V. Push"), choices=ROW_CHOICES, default=DEFAULT_CHOICE)
    vertical_pull = models.IntegerField(verbose_name=_("V. Pull"),
                                        choices=ROW_CHOICES, default=DEFAULT_CHOICE)
    style = models.IntegerField(
        verbose_name=_("Style"), choices=STYLE_CHOICES, default=DEFAULT_CHOICE)
    border = models.IntegerField(
        verbose_name=_("Border"), choices=BORDER_CHOICES, default=DEFAULT_CHOICE)
    clear = models.IntegerField(
        verbose_name=_("Clear"), choices=CLEAR_CHOICES, default=DEFAULT_CHOICE)
    last = models.NullBooleanField(verbose_name=_('Is last?'))
    visible = models.NullBooleanField(verbose_name=_('Is visible?'))

    class Meta:
        abstract = True
        verbose_name = _("abstract widget")
        verbose_name_plural = _("abstract widgets")

    def thumb_geom(self):
        return config_value('MEDIA', 'THUMB_MEDIUM_GEOM')

    def thumb_options(self):
        return config_value('MEDIA', 'THUMB_MEDIUM_OPTIONS')

    def _render_box_classes(self):
        classes = []
        options = self.options
        try:
            if options['align'][0] != 'a':
                classes.append('align-%s' % options['align'][0])
            if options['align'][1] != 'a':
                classes.append('valign-%s' % options['align'][1])
            if options['size'][0] > 0:
                classes.append('span-%s' % options['size'][0])
            if options['size'][1] > 0:
                classes.append('vspan-%s' % options['size'][1])
            if options['padding'][0] > 0:
                classes.append('vprepend-%s' % options['padding'][0])
            if options['padding'][1] > 0:
                classes.append('append-%s' % options['padding'][1])
            if options['padding'][2] > 0:
                classes.append('vappend-%s' % options['padding'][2])
            if options['padding'][3] > 0:
                classes.append('prepend-%s' % options['padding'][3])
            if options['margin'][0] > 0:
                classes.append('vpull-%s' % options['margin'][0])
            if options['margin'][1] > 0:
                classes.append('push-%s' % options['margin'][1])
            if options['margin'][2] > 0:
                classes.append('vpush-%s' % options['margin'][2])
            if options['margin'][3] > 0:
                classes.append('pull-%s' % options['margin'][3])
            if options['clear'] == 'l':
                classes.append('clearfix')
            if options['clear'] == 'f':
                classes.append('clear')
            if options['border'] == '1':
                classes.append('border')
            if options['border'] == '2':
                classes.append('colborder')
            if options['style'] == '' or options['style'] == None:
                classes.append('normal-widget')
            else:
                classes.append('%s-widget' % options['style'])
            if options['last']:
                classes.append('last')
        except:
            classes.append('widget-error')
        return u' '.join(classes)
    render_box_classes = property(_render_box_classes)

    def get_template_name(self, format='html'):
        return self.template_name

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
        #        if options.has_key('use_xml') and options['use_xml']:
        #            template = loader.get_template(self.template_xml_name)
        if options.has_key('format'):
            format = options.get('format')
            base_template = 'widget/doc_base.%s' % format

        else:
            format = 'html'
            base_template = 'widget/base.%s' % format

        template = loader.get_template(self.get_template_name(format))

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

    def save(self, *args, **kwargs):
        super(Widget, self).save(*args, **kwargs)
        if self.options == {}:
            self.options = DEFAULT_DISPLAY_OPTIONS
            self.save()

    def model_cls(self):
        return self.__class__.__name__

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
            f.name for f in Widget._meta.fields
            if f.name not in ['options', 'prerendered_content']]

        return fields_for_model(
                cls, exclude=widget_fields +
                [], widgets=WIDGETS)
