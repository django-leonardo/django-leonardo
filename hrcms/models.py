# -#- coding: utf-8 -#-
from functools import update_wrapper

import six
from admin_tools.menu import items, Menu
from django import http, template
from django.conf import settings
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
from feincms.module.page.models import Page
from hrcms.signals import page_check_options
from livesettings import config_value

pre_save.connect(page_check_options, sender=Page)

from django.contrib import admin


class WebCmsAdminSite(AdminSite):

    def get_urls(self):
        from django.conf.urls import url, include
        # Since this module gets imported in the application's root package,
        # it cannot import models from other applications at the module level,
        # and django.contrib.contenttypes.views imports ContentType.
        from django.contrib.contenttypes import views as contenttype_views

        if settings.DEBUG:
            self.check_dependencies()

        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)
            wrapper.admin_site = self
            return update_wrapper(wrapper, view)

        # Admin-site-wide views.
        urlpatterns = [
            url(r'^$', wrap(self.index), name='index'),
            url(r'^login/$', self.login, name='login'),
            url(r'^logout/$', wrap(self.logout), name='logout'),
            url(r'^password_change/$', wrap(self.password_change, cacheable=True), name='password_change'),
            url(r'^password_change/done/$', wrap(self.password_change_done, cacheable=True),
                name='password_change_done'),
            url(r'^jsi18n/$', wrap(self.i18n_javascript, cacheable=True), name='jsi18n'),
            url(r'^r/(?P<content_type_id>\d+)/(?P<object_id>.+)/$', wrap(contenttype_views.shortcut),
                name='view_on_site'),
        ]

        # Add in each model's views, and create a list of valid URLS for the
        # app_index
        valid_app_labels = []
        for model, model_admin in six.iteritems(self._registry):
            urlpatterns += [
                url(r'^%s/%s/' % (model._meta.app_label, model._meta.model_name), include(model_admin.urls)),
            ]
            if model._meta.app_label not in valid_app_labels:
                valid_app_labels.append(model._meta.app_label)

        for model, model_admin in six.iteritems(admin.site._registry):
            urlpatterns += [
                url(r'^%s/%s/' % (model._meta.app_label, model._meta.model_name), include(model_admin.urls)),
            ]
            if model._meta.app_label not in valid_app_labels:
                valid_app_labels.append(model._meta.app_label)


        # If there were ModelAdmins registered, we should have a list of app
        # labels for which we need to allow access to the app_index view,
        if valid_app_labels:
            regex = r'^(?P<app_label>' + '|'.join(valid_app_labels) + ')/$'
            urlpatterns += [
                url(regex, wrap(self.app_index), name='app_list'),
            ]
        return urlpatterns

webcms_admin = WebCmsAdminSite(name="admin")

# rename
hrcms_admin = webcms_admin

COLUMN_CHOICES = (
    (0, u' — '),
    (1, _('1 col')),
    (2, _('2 cols')),
    (3, _('3 cols')),
    (4, _('4 cols')),
    (5, _('5 cols')),
    (6, _('6 cols')),
    (7, _('7 cols')),
    (8, _('8 cols')),
    (9, _('9 cols')),
    (10, _('10 cols')),
    (11, _('11 cols')),
    (12, _('12 cols')),
    (13, _('13 cols')),
    (14, _('14 cols')),
    (15, _('15 cols')),
    (16, _('16 cols')),
    (17, _('17 cols')),
    (18, _('18 cols')),
    (19, _('19 cols')),
    (20, _('20 cols')),
    (21, _('21 cols')),
    (22, _('22 cols')),
    (23, _('23 cols')),
    (24, _('24 cols')),
)

ROW_CHOICES = (
    (0, u' — '),
    (1, _('1 row')),
    (2, _('2 rows')),
    (3, _('3 rows')),
    (4, _('4 rows')),
    (5, _('5 rows')),
    (6, _('6 rows')),
    (7, _('7 rows')),
    (8, _('8 rows')),
    (9, _('9 rows')),
    (10, _('10 rows')),
    (11, _('11 rows')),
    (12, _('12 rows')),
    (13, _('13 rows')),
    (14, _('14 rows')),
    (15, _('15 rows')),
    (16, _('16 rows')),
    (17, _('17 rows')),
    (18, _('18 rows')),
    (19, _('19 rows')),
    (20, _('20 rows')),
    (21, _('21 rows')),
    (22, _('22 rows')),
    (23, _('23 rows')),
    (24, _('24 rows')),
)

CLEAR_CHOICES = (
    ('', _('none')),
    ('f', _('break before')),
    ('l', _('break after')),
)

BORDER_CHOICES = (
    ('0', _('no border')),
    ('1', _('border')),
    ('2', _('wide border')),
)

ALIGN_CHOICES = (
    ('a', _('auto')),
    ('l', _('left')),
    ('c', _('center')),
    ('r', _('right')),
)

VERTICAL_ALIGN_CHOICES = (
    ('a', _('auto')),
    ('t', _('top')),
    ('m', _('middle')),
    ('b', _('bottom')),
)

STYLE_CHOICES = (
    ('', _('none')),
    ('nested_box', _('nested_box')),
    ('padded', _('padded')),
    ('boxed', _('single box')),
    ('boxed-top', _('box top')),
    ('boxed-middle', _('box middle')),
    ('boxed-bottom', _('box bottom')),
)

DEFAULT_DISPLAY_OPTIONS = {
    'label': None,
    'template_name': 'default',
    'style': None,
    'size': [24, 0],
    'align': ["a", "a"],
    'padding': [0, 0, 0, 0],
    'margin': [0, 0, 0, 0],
    'visible': True,
    'border': None,
    'clear': None,
    'last': False,
}

class Widget(models.Model):
    options = JSONField(verbose_name=_('widget options'), blank=True, editable=False)
    prerendered_content = models.TextField(_('prerendered content'), blank=True, editable=False)

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
