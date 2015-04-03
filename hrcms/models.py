# -#- coding: utf-8 -#-
from functools import update_wrapper

import six
from admin_tools.menu import items, Menu
from django import http, template
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django_assets import Bundle, register
from django_extensions.db.fields.json import JSONField
from feincms.module.page.models import BasePage as FeinCMSPage
from feincms.models import Base as FeinCMSBase

from .const import *


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


class Widget(FeinCMSBase):
    options = JSONField(
        verbose_name=_('widget options'), blank=True, editable=False)
    prerendered_content = models.TextField(
        _('prerendered content'), blank=True, editable=False)

    label = models.CharField(verbose_name=_("Title"), max_length=255)
    template_name = models.CharField(
        verbose_name=_("Display"), max_length=255)

    span = models.IntegerField(verbose_name=_("Span"),
        choices=COLUMN_CHOICES, default=DEFAULT_WIDTH)
    vertical_span = models.IntegerField(verbose_name=_("V. Span"),
        choices=ROW_CHOICES, default=DEFAULT_WIDTH)
    align = models.IntegerField(verbose_name=_("Alignment"), choices=ALIGN_CHOICES)
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

    def _template_name(self):
        try:
            if self.options['template_name'] == '':
                template = 'default'
            else:
                template = self.options['template_name']
        except:
            template = 'default'
        return u'widget/%s/%s.html' % (self.widget_name, template)
    template_name = property(_template_name)

    def get_template_name(self, format):
        try:
            if self.options['template_name'] == '':
                template = 'default'
            else:
                template = self.options['template_name']
        except:
            template = 'default'
        return u'widget/%s/%s.%s' % (self.widget_name, template, format)
    template_name = property(_template_name)

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
        if self.prerendered_content == '':
            return self.render_content(kwargs)
        else:
            return self.prerendered_content

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
"""
jquery_js = Bundle(
    'lib/jquery/1.6/js/jquery.js', # 1.6.2
    'lib/jquery/1.4/js/hoverIntent.js', # r6
    'lib/jquery/1.4/js/notice.js', # 1.0.1
    'lib/jquery/1.4/js/cookie.js',
    'lib/jquery/1.4/js/form.js',
    'lib/jquery/1.4/js/blockUI.js', # 2.37
    'lib/jquery/1.4/js/hslides.js', # 1.0
    'lib/jquery/1.4/js/cycle.all.js', # 2.97
    'lib/jquery/1.6/js/color.js',
    'lib/jquery/1.4/js/timers.js',
    'lib/jquery/1.4/js/easing.js',
    'lib/jquery/1.4/js/jcarousel.js', # 0.2.8
    'lib/jquery/1.4/js/lavalamp.js',
    'lib/jquery/1.4/js/panelgallery.js',
    'lib/jquery/1.4/js/dajax.core.js',
    'lib/jquery/1.4/js/colorbox.js',
    'lib/jquery/1.4/js/rating.js', # 3.13
    'lib/jquery/1.4/js/superfish.js', # 1.4.8
    'lib/jquery/1.4/js/supersubs.js', # 0.2b
    'lib/swfobject/swfobject.js', # 2011-02-23
    'lib/utils/json2.js', # 2011-02-23
    'lib/utils/DD_belatedPNG.js', # 0.0.8a
    filters='jsmin',
    output='_cache/jquery.js'
)
register('jquery_js', jquery_js)

jquery_ui_js = Bundle(
    # core
    'lib/jquery-ui/1.9/js/ui.core.js',
    'lib/jquery-ui/1.9/js/ui.widget.js',
    'lib/jquery-ui/1.9/js/ui.mouse.js',
    'lib/jquery-ui/1.9/js/ui.position.js',
    'lib/jquery-ui/1.9/js/ui.draggable.js',
    'lib/jquery-ui/1.9/js/ui.sortable.js',
    'lib/jquery-ui/1.9/js/ui.droppable.js',
    'lib/jquery-ui/1.9/js/ui.resizable.js',
    # widgets
    'lib/jquery-ui/1.9/js/ui.button.js',
    'lib/jquery-ui/1.9/js/ui.dialog.js',
    'lib/jquery-ui/1.9/js/ui.slider.js',
    'lib/jquery-ui/1.9/js/ui.tabs.js',
    'lib/jquery-ui/1.9/js/ui.autocomplete.js',
    'lib/jquery-ui/1.9/js/ui.datepicker.js',
    'lib/jquery-ui/1.9/js/ui.tooltip.js',
    filters='jsmin',
    output='_cache/jquery_ui.js'
)
register('jquery_ui_js', jquery_ui_js)

jquery_ui_css = Bundle(
    'lib/jquery-ui-themes/absolution/jquery.ui.base.css',
    'lib/jquery-ui-themes/absolution/jquery.ui.core.css',
    'lib/jquery-ui-themes/absolution/jquery.ui.resizable.css',
    'lib/jquery-ui-themes/absolution/jquery.ui.selectable.css',
    'lib/jquery-ui-themes/absolution/jquery.ui.autocomplete.css',
    'lib/jquery-ui-themes/absolution/jquery.ui.button.css',
    'lib/jquery-ui-themes/absolution/jquery.ui.dialog.css',
    'lib/jquery-ui-themes/absolution/jquery.ui.tabs.css',
    'lib/jquery-ui-themes/absolution/jquery.ui.slider.css',
    'lib/jquery-ui-themes/absolution/jquery.ui.datepicker.css',
    'lib/jquery-ui-themes/absolution/jquery.ui.tooltip.css',
    'lib/jquery-ui-themes/absolution/colors/jquery.ui.colors.blue.css',
    filters='cssmin,cssrewrite',
    output='_cache/jquery_ui.css'
)
register('jquery_ui_css', jquery_ui_css)

blueprint_css = Bundle(
    'lib/blueprint/1.0/css/screen.css',
    'lib/blueprint/1.0/css/plugins/vertical-positioning/screen.css',
    'lib/blueprint/1.0/css/plugins/liquid/liquid.css',
    filters='cssmin,cssrewrite',
    output='_cache/blueprint.css'
)
register('blueprint_css', blueprint_css)

webcms_js = Bundle(
    'lib/webcms/js/forms.js',
    filters='jsmin',
    output='_cache/webcms.js'
)
register('webcms_js', webcms_js)

webcms_css = Bundle(
    'lib/webcms/css/forms.css',
    'lib/webcms/css/highlight.css',
    'lib/jquery/1.4/css/rating.css',
    filters='cssmin,cssrewrite',
    output='_cache/webcms.css'
)
register('webcms_css', webcms_css)

webcms_fe_js = Bundle(
    'lib/jquery/1.4/js/stylesheetToggle.js',
    'lib/jquery/1.6/js/griddy.js',
    'lib/jstree/1.0/jstree.js',
    'lib/webcms/js/frontend_editing.js',
    filters='jsmin',
    output='_cache/webcms_fe.js'
)
register('webcms_fe_js', webcms_fe_js)

webcms_fe_css = Bundle(
    'lib/webcms/css/frontend_editing.css',
    'lib/jstree/1.0/themes/default/style.css',
    filters='cssmin,cssrewrite',
    output='_cache/webcms_fe.css'
)
register('webcms_fe_css', webcms_fe_css)

webcms_admin_js = Bundle(
    'lib/tinymce/3.4/tiny_mce.js',
    'lib/tinymce/3.4/jquery.tinymce.js',
    filters='jsmin',
    output='_cache/webcms_admin.js'
)
register('webcms_admin_js', webcms_admin_js)

webcms_admin_css = Bundle(
    'lib/codemirror2/codemirror.css',
    filters='cssmin,cssrewrite',
    output='_cache/webcms_admin.css'
)
register('webcms_admin_css', webcms_admin_css)
"""
