
from leonardo.module.web.models import Widget
from leonardo.module.nav.mixins import NavigationWidgetMixin
from feincms.module.page.extensions.navigation import (NavigationExtension,
                                                       PagePretender)
from django.utils.translation import ugettext_lazy as _


class NavigationWidget(Widget, NavigationWidgetMixin):

    """Base class for navigation widgets
    """

    class Meta:
        abstract = True


class FlatPageContentNavigationExtension(NavigationExtension):
    name = _('Flat page content navigation')

    def children(self, page, **kwargs):
        base_url = page.get_absolute_url()
        widget_list = page.objects.filter(parent=None)
        for widget in widget_list:
            subchildren = []
            for subwidget in widget.media_folder_children.all():
                subchildren.append(PagePretender(
                    title=subwidget,
                    url='%s%s/%s/' % (base_url, widget.name, subwidget.name),
                    level=5
                ))
            yield PagePretender(
                title=widget,
                url='%s%s/' % (base_url, widget.name),
                children=subchildren,
                level=5
            )


class NestedPageContentNavigationExtension(NavigationExtension):
    name = _('Nested page content navigation')

    def children(self, page, **kwargs):
        base_url = page.get_absolute_url()
        widget_list = page.objects.filter(parent=None)
        for widget in widget_list:
            subchildren = []
            for subwidget in widget.media_folder_children.all():
                subchildren.append(PagePretender(
                    title=subwidget,
                    url='%s%s/%s/' % (base_url, widget.name, subwidget.name),
                    level=5
                ))
            yield PagePretender(
                title=widget,
                url='%s%s/' % (base_url, widget.name),
                children=subchildren,
                level=5
            )
