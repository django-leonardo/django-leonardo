
from __future__ import unicode_literals

import logging
from django.db import models
from django.utils.encoding import python_2_unicode_compatible, smart_text
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from feincms.module.page.models import BasePage as FeinCMSPage
from django.core.exceptions import PermissionDenied
from leonardo.module.web.page.utils import get_anonymous_request
from ..const import *
from ..processors import edit as edit_processors

LOG = logging.getLogger(__name__)


@python_2_unicode_compatible
class PageDimension(models.Model):

    page = models.ForeignKey('Page', verbose_name=_('Page'))
    size = models.CharField(
        verbose_name="Size", max_length=20,
        choices=DISPLAY_SIZE_CHOICES, default='md')
    col1_width = models.IntegerField(
        verbose_name=_("Column 1 width"),
        choices=COLUMN_CHOICES, default=DEFAULT_WIDTH)
    col2_width = models.IntegerField(
        verbose_name=_("Column 2 width"),
        choices=COLUMN_CHOICES, default=DEFAULT_WIDTH)
    col3_width = models.IntegerField(
        verbose_name=_("Column 3 width"),
        choices=COLUMN_CHOICES, default=DEFAULT_WIDTH)

    def __str__(self):
        return "{0} - {1}".format(self.page, self.size)

    class Meta:
        verbose_name = _("Page dimension")
        verbose_name_plural = _("Page dimensions")
        app_label = "web"


@python_2_unicode_compatible
class PageTheme(models.Model):

    name = models.CharField(
        verbose_name=_("Name"), max_length=255, null=True, blank=True)
    label = models.CharField(
        verbose_name=_("Title"), max_length=255, null=True, blank=True)
    template = models.ForeignKey(
        'dbtemplates.Template',
        verbose_name=_('Template'),
        related_name='page_templates',
        limit_choices_to={'name__startswith': "base/page/"})
    styles = models.TextField(verbose_name=_('Style'), blank=True)

    def __str__(self):
        return self.label or super(PageTheme, self).__str__()

    class Meta:
        verbose_name = _("Page theme")
        verbose_name_plural = _("Page themes")
        app_label = "web"


@python_2_unicode_compatible
class PageColorScheme(models.Model):

    name = models.CharField(
        verbose_name=_("Name"), max_length=255, null=True, blank=True)
    label = models.CharField(
        verbose_name=_("Title"), max_length=255, null=True, blank=True)
    styles = models.TextField(verbose_name=_('Styles'), blank=True)
    variables = models.TextField(verbose_name=_('variables'), blank=True)
    theme = models.ForeignKey(
        PageTheme, verbose_name=_('Template'), related_name='templates')

    def __str__(self):
        return self.label or super(PageColorScheme, self).__str__()

    class Meta:
        verbose_name = _("Page color scheme")
        verbose_name_plural = _("Page color schemes")
        app_label = "web"


class Page(FeinCMSPage):

    layout = models.CharField(
        verbose_name=_("Layout"), max_length=25,
        default='fixed', choices=PAGE_LAYOUT_CHOICES)
    theme = models.ForeignKey(PageTheme, verbose_name=_('Theme'))
    color_scheme = models.ForeignKey(
        PageColorScheme, verbose_name=_('Color scheme'))

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")
        ordering = ['tree_id', 'lft']
        app_label = "web"

    @cached_property
    def tree_label(self):
        '''render tree label like as `root > child > child`'''
        titles = []
        page = self
        while page:
            titles.append(page.title)
            page = page.parent
        return smart_text(' > '.join(reversed(titles)))

    @cached_property
    def own_dimensions(self):
        self_dimensions = PageDimension.objects.filter(
            page=self)
        return self_dimensions

    @cached_property
    def dimensions(self):
        # collect all dimensions
        self_dimensions = self.own_dimensions
        if self_dimensions.exists():
            return self_dimensions
        parent_dimensions = None
        if self.parent and self.parent.template_key == self.template_key:
            parent_dimensions = self.parent.dimensions
        parent_dimensions = parent_dimensions or PageDimension.objects.none()
        return parent_dimensions

    def delete(self, *args, **kwargs):
        super(Page, self).delete(*args, **kwargs)
        [d.delete() for d in self.own_dimensions]

    @cached_property
    def get_base_template(self):
        return self.theme.template

    def get_next_ordering(self, region):
        """return order for new CT in region
        """
        return len(getattr(self.content, region, [])) + 1

    @cached_property
    def get_layout_class(self):
        if self.layout == 'fluid':
            return 'container-fluid'
        else:
            return 'container'

    @cached_property
    def get_all_col_classes(self):
        STR = "col-{0}-{1}"
        return [{'col1': STR.format(d.size, d.col1_width),
                 'col2': STR.format(d.size, d.col2_width),
                 'col3': STR.format(d.size, d.col3_width)}
                for d in self.dimensions]

    def get_col_classes(self, col='col1'):
        return " ".join([
            classes.get(col)
            for classes in self.get_all_col_classes])

    def flush_ct_inventory(self):
        """internal method used only if ct_inventory is enabled
        """
        if hasattr(self, '_ct_inventory'):

            # skip self from update
            self._ct_inventory = None
            self.update_view = False
            self.save()

            # for instance in self.get_descendants(include_self=False):
            #     instance._ct_inventory = None
            #     instance.save()

    @classmethod
    def register_default_processors(cls, frontend_editing=None):
        """
        Register our default request processors for the out-of-the-box
        Page experience.

        Since FeinCMS 1.11 was removed from core.

        """
        super(Page, cls).register_default_processors()

        if frontend_editing:
            cls.register_request_processor(
                edit_processors.frontendediting_request_processor,
                key='frontend_editing')
            cls.register_response_processor(
                edit_processors.frontendediting_response_processor,
                key='frontend_editing')

    def run_request_processors(self, request):
        """
        Before rendering a page, run all registered request processors. A
        request processor may peruse and modify the page or the request. It can
        also return a ``HttpResponse`` for shortcutting the rendering and
        returning that response immediately to the client.
        """
        if not getattr(self, 'request_processors', None):
            return

        for fn in reversed(list(self.request_processors.values())):
            r = fn(self, request)
            if r:
                return r

    @property
    def as_text(self):
        '''Fetch and render all regions

        For search and test purposes

        just a prototype
        '''
        from leonardo.templatetags.leonardo_tags import _render_content

        request = get_anonymous_request(self)

        content = ''

        try:

            for region in [region.key
                           for region in self._feincms_all_regions]:
                content += ''.join(
                    _render_content(content, request=request, context={})
                    for content in getattr(self.content, region))
        except PermissionDenied:
            pass
        except Exception as e:
            LOG.exception(e)

        return content

    @cached_property
    def cls_name(self):
        return '%s.%s' % (self._meta.app_label,
                          self.__class__.__name__)
