
import sys

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.cache import caches
from django.db import models
from django.forms.models import fields_for_model
from django.template import RequestContext, loader
from django.template.loader import render_to_string
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from feincms.admin.item_editor import FeinCMSInline
from feincms.models import Base as FeinCMSBase
from leonardo.utils.memoized import widget_memoized
from leonardo.utils.templates import find_all_templates, template_choices
from ..processors.config import context_config
from ..const import *
from ..widgets.const import ENTER_EFFECT_CHOICES, WIDGET_COLOR_SCHEME_CHOICES
from ..widgets.forms import WIDGETS, WidgetForm
from ..widgets.mixins import ContentProxyWidgetMixin, ListWidgetMixin

try:
    from django.contrib.contenttypes import generic
except ImportError:
    from django.contrib.contenttypes.fields import GenericForeignKey


class WidgetInline(FeinCMSInline):
    form = WidgetForm

    template = 'admin/leonardo/widget_inline.html'

    def formfield_for_dbfield(self, db_field, request, **kwargs):

        widget = self.model.get_widget_for_field(db_field.name)

        if widget:
            kwargs['widget'] = widget
            return db_field.formfield(**kwargs)

        return super(WidgetInline, self).formfield_for_dbfield(
            db_field, request=request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "base_theme":
            queryset = WidgetBaseTheme.objects.all()
            kwargs["queryset"] = queryset.exclude(name__startswith="_")
            kwargs["initial"] = queryset.first()
        if db_field.name == "content_theme":
            queryset = WidgetContentTheme.objects.filter(
                widget_class=self.model.__name__)
            kwargs["queryset"] = queryset.exclude(name__startswith="_")
            kwargs["initial"] = queryset.first()
        form_field = super(WidgetInline, self).formfield_for_foreignkey(
            db_field, request, **kwargs)
        # bootstrap field
        form_field.widget.attrs['class'] = 'form-control'
        return form_field

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
                    ('label', 'base_theme', 'content_theme',
                     'layout', 'align', 'enabled', 'color_scheme'),
                ],
            }),
            (_('Effects'), {
                'fields': [
                    ('enter_effect_style', 'enter_effect_duration',
                     'enter_effect_delay', 'enter_effect_offset',
                     'enter_effect_iteration', 'enabled',),
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
                                 choices=ROW_CHOICES, default=0)
    offset = models.IntegerField(verbose_name=_("Offset"),
                                 choices=COLUMN_CHOICES, default=0)

    @cached_property
    def classes(self):
        classes = []
        classes.append('col-{}-{}'.format(self.size, self.width))
        if self.height != 0:
            classes.append('row-{}-{}'.format(self.size, self.height))
        classes.append('col-{}-offset-{}'.format(self.size, self.offset))
        return ' '.join(classes)

    def __str__(self):
        return "{0} - {1}".format(self.widget_type, self.classes)

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
        'dbtemplates.Template', verbose_name=_('Content template'),
        related_name='content_templates', limit_choices_to={'name__startswith': "widget/"})
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
        'dbtemplates.Template', verbose_name=_('Base template'),
        related_name='base_templates', limit_choices_to={'name__startswith': "base/widget/"})

    style = models.TextField(verbose_name=_('Base style'), blank=True)

    def __str__(self):
        return self.label or str(self._meta.verbose_name + ' %s' % self.pk)

    class Meta:
        verbose_name = _("Widget base theme")
        verbose_name_plural = _("Widget base themes")


@python_2_unicode_compatible
class Widget(FeinCMSBase):

    feincms_item_editor_inline = WidgetInline

    prerendered_content = models.TextField(
        verbose_name=_('prerendered content'), blank=True)
    enabled = models.NullBooleanField(
        verbose_name=_('Is visible?'), default=True)
    label = models.CharField(
        verbose_name=_("Title"), max_length=255, null=True, blank=True)
    base_theme = models.ForeignKey(
        WidgetBaseTheme, verbose_name=_('Base theme'),
        related_name="%(app_label)s_%(class)s_related")
    content_theme = models.ForeignKey(
        WidgetContentTheme, verbose_name=_('Content theme'),
        related_name="%(app_label)s_%(class)s_related")
    layout = models.CharField(
        verbose_name=_("Layout"), max_length=25,
        default='inline', choices=WIDGET_LAYOUT_CHOICES)
    align = models.CharField(
        verbose_name=_("Alignment"), max_length=25,
        default='left', choices=WIDGET_ALIGN_CHOICES)
    vertical_align = models.CharField(
        verbose_name=_("Vertical Alignment"), max_length=25,
        default='top', choices=VERTICAL_ALIGN_CHOICES)

    # common attributes
    enter_effect_style = models.CharField(
        verbose_name=_("Enter effect style"),
        max_length=25, default='disabled', choices=ENTER_EFFECT_CHOICES)

    enter_effect_duration = models.PositiveIntegerField(verbose_name=_(
        'Enter Effect Duration'), null=True, blank=True)
    enter_effect_delay = models.PositiveIntegerField(null=True, blank=True)
    enter_effect_offset = models.PositiveIntegerField(null=True, blank=True)
    enter_effect_iteration = models.PositiveIntegerField(null=True, blank=True)

    color_scheme = models.CharField(
        verbose_name=_("Color scheme"),
        max_length=25, default='default', choices=WIDGET_COLOR_SCHEME_CHOICES)

    def save(self, created=True, *args, **kwargs):

        if self.pk is None and created:
            self.created = True

        super(Widget, self).save(*args, **kwargs)

        if not self.dimensions.exists() and created:
            WidgetDimension(**{
                'widget_id': self.pk,
                'widget_type': self.content_type,
            }).save()

        self.purge_from_cache()

    def delete(self, *args, **kwargs):
        super(Widget, self).delete(*args, **kwargs)
        [d.delete() for d in self.dimensions]

    class Meta:
        abstract = True
        verbose_name = _("Abstract widget")
        verbose_name_plural = _("Abstract widgets")

    def __str__(self):
        return self.label or (
            '%s<pk=%s, parent=%s<pk=%s, %s>, region=%s,'
            ' ordering=%d>') % (
            self.__class__.__name__,
            self.pk,
            self.parent.__class__.__name__,
            self.parent.pk,
            self.parent,
            self.region,
            self.ordering)

    @cached_property
    def get_ct_name(self):
        """returns content type name with app label
        """
        return ".".join([self._meta.app_label, self._meta.model_name])

    @cached_property
    def content_type(self):
        return ContentType.objects.get_for_model(self)

    def thumb_geom(self):
        return config_value('MEDIA', 'THUMB_MEDIUM_GEOM')

    def thumb_options(self):
        return config_value('MEDIA', 'THUMB_MEDIUM_OPTIONS')

    def get_template_name(self):
        return self.content_theme.template

    @cached_property
    def get_template(self):
        return self.content_theme.template

    def _template_xml_name(self):
        template = 'default'
        return u'widget/%s/%s.xml' % (self.widget_name, template)
    template_xml_name = property(_template_xml_name)

    @property
    def widget_name(self):
        return self.__class__.__name__.lower().replace('widget', '')

    @cached_property
    def get_base_template(self):
        return self.base_theme.template

    @cached_property
    def widget_label(self):
        return self._meta.verbose_name

    @cached_property
    def template_source(self):
        template = loader.get_template(self.content_theme.template)
        return template

    def render(self, **kwargs):
        return self.render_content(kwargs)

    @widget_memoized
    def render_with_cache(self, options):
        """proxy for render_content with memoized

        this method provide best performence for complicated
        widget content like a context navigation
        """
        return self.render_content(options)

    def get_template_data(self, request):
        '''returns dictionary
        use this method for providing context data
        '''
        return {}

    def get_context_data(self, request):
        '''returns initial context'''

        context = {
            'widget': self,
            'base_template': self.get_base_template,
            'request': request,
            'LEONARDO_CONFIG': context_config
        }
        context.update(self.get_template_data(request))
        return context

    def render_content(self, options):
        '''returns rendered widget and handle error during rendering'''

        request = options.get('request', {})
        context = self.get_context_data(request)

        try:
            rendered_content = self.template_source.render(context)
        except Exception as e:
            if settings.DEBUG:
                exc_info = sys.exc_info()
                raise six.reraise(*exc_info)
            rendered_content = self.render_error(context, e)
        return rendered_content

    def render_error(self, context, exception):
        return render_to_string("widget/error.html", {
            'context': context,
            'error': str(exception),
        })

    def render_response(self, context={}):
        '''just render to string shortcut for less imports'''
        return render_to_string(self.get_template_name, context)

    @cached_property
    def model_cls(self):
        return self.__class__.__name__

    @cached_property
    def dimensions(self):
        return WidgetDimension.objects.filter(
            widget_id=self.pk,
            widget_type=ContentType.objects.get_for_model(self))

    @cached_property
    def get_dimension_classes(self):
        """agreggate all css classes
        """
        classes = []
        for d in self.dimensions:
            # do not duplicate same classes
            for cls in d.classes.split(' '):
                if cls not in classes:
                    classes.append(cls)
        return classes

    @cached_property
    def render_content_classes(self):
        """agreggate all css classes
        """
        classes = [
            'leonardo-content',
            'template-%s' % self.content_theme.name,
            '%s-content-%s' % (self.widget_name, self.content_theme.name)
        ]
        if self.vertical_align == "middle":
          classes.append("centered")
        return " ".join(classes)

    def get_classes(self):
        '''return array of custom widget classes'''
        if hasattr(self, 'classes') and isinstance(self.classes, str):
            return self.classes.split(' ')
        return []

    @cached_property
    def render_base_classes(self):
        """agreggate all css classes
        """
        classes = self.get_dimension_classes
        classes.append('%s-base-%s' % (self.widget_name, self.base_theme.name))
        classes.append('leonardo-widget')
        classes.append('leonardo-%s-widget' % self.widget_name)
        classes.append( "text-%s" % self.align)
        if getattr(self, 'auto_reload', False):
            classes.append('auto-reload')
        if self.vertical_align == 'middle':
            classes.append("valignContainer")
        return " ".join(classes + self.get_classes())

    @classmethod
    def get_widget_for_field(cls, name):
        '''returns widget for field
        if has widgets declared
        support function instead of widgets
        '''
        if hasattr(cls, 'widgets') and name in cls.widgets:
            widget = cls.widgets[name]
            if callable(widget):
                widget = widget()
                # save for later
                if widget:
                    cls.widgets[name] = widget
            return widget
        return

    @classmethod
    def init_widgets(cls):
        '''init all widget widgets
        '''
        if hasattr(cls, 'widgets'):
            for field, widget in cls.widgets.items():
                if callable(widget):
                    widget = widget()
                    if widget:
                        cls.widgets[field] = widget

    @classmethod
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

    @property
    def next_ordering(self):
        """return order for creating in content region
        """
        if self.parent:
            return len(getattr(self.parent.content, self.region, [])) + 1
        else:
            return 0

    @cached_property
    def fe_identifier(self):
        """
        Returns an identifier which is understood by the frontend
        editing javascript code. (It is used to find the URL which
        should be used to load the form for every given block of
        content.)
        """
        meta = self.__class__._meta
        return '%s-%s-%s-%s' % (
            meta.app_label,
            meta.model_name,
            self.parent_id,
            self.id,
        )

    @classmethod
    def get_widget_icon(cls):
        return getattr(cls, 'icon', 'fa fa-plus')

    # CACHE TOOLS

    @cached_property
    def cache(self):
        '''default cache'''
        return caches['default']

    @cached_property
    def cache_key(self):
        '''default key for html content'''
        return 'widget.%s.html' % self.fe_identifier

    @cached_property
    def cache_keys(self):
        '''Returns all cache keys which would be
        flushed after save
        '''
        return [self.cache_key]

    @cached_property
    def widget_cache_timeout(self):
        '''allow widget to set custom cache timeout'''
        return getattr(self, 'cache_timeout', settings.LEONARDO_CACHE_TIMEOUT)

    def is_cached(self, request):
        '''returns True if widget will be cached or not
        in the deafult state returns False and it's driven
        by ``leonardo_cache`` property
        '''
        if request.frontend_editing:
            return False
        return getattr(self, 'leonardo_cache', False)

    def purge_from_cache(self):
        '''Purge widget content from cache'''

        self.cache.delete_many(self.cache_keys)


class ListWidget(Widget, ListWidgetMixin):

    """Base class for object list widget
    """
    class Meta:
        abstract = True
