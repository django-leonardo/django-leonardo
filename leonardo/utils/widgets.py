from __future__ import absolute_import

from django import forms
from django.conf import settings
from django.utils import six
from importlib import import_module


def load_widget_classes(widgets):

    _widgets = []

    def get_class_from_string(widget):
        mod = '.'.join(widget.split('.')[0:-1])
        cls_name = widget.split('.')[-1]
        return mod, cls_name

    for widget in widgets:

        kwargs = {}

        # load class from strings
        if isinstance(widget, six.string_types):
            try:
                mod, cls_name = get_class_from_string(widget)
                WidgetCls = getattr(import_module(mod), cls_name)
            except Exception as e:
                raise e
        elif isinstance(widget, tuple):
            try:
                mod, cls_name = get_class_from_string(widget[0])
                if len(widget) > 1:
                    kwargs.update(widget[1])
                WidgetCls = getattr(import_module(mod), cls_name)
            except Exception as e:
                raise Exception('%s: %s' % (mod, e))
        else:
            WidgetCls = widget

        _widgets.append(WidgetCls)

    return _widgets


def get_all_widget_classes():
    """returns collected Leonardo Widgets

    if not declared in settings is used __subclasses__
    which not supports widget subclassing

    """
    from leonardo.module.web.models import Widget
    _widgets = getattr(settings,
                       'WIDGETS', Widget.__subclasses__())
    widgets = []
    if isinstance(_widgets, dict):
        for group, widget_cls in six.iteritems(_widgets):
            widgets.extend(widget_cls)
    elif isinstance(_widgets, list):
        widgets = _widgets
    return load_widget_classes(widgets)


def get_grouped_widgets(feincms_object, request=None):
    '''returns tuple(choices, grouped, ungrouped)

    requires feincms_object for getting content types

    request optionaly for checking permissions, but not required

    grouped = {'web': (id, label, icon)}
    '''

    grouped = {}
    ungrouped = []
    choices = []

    for ct in feincms_object._feincms_content_types:
        # Skip cts that we shouldn't be adding anyway
        opts = ct._meta
        # check permissions
        if request and request.user:
            from django.contrib.auth import get_permission_codename
            perm = opts.app_label + "." + \
                get_permission_codename('add', opts)
            if not request.user.has_perm(perm):
                continue

        ct_info = ('.'.join([ct._meta.app_label,
                             ct.__name__.lower()]),
                   ct._meta.verbose_name,
                   ct.get_widget_icon)
        if hasattr(ct, 'optgroup'):
            if ct.optgroup in grouped:
                grouped[ct.optgroup].append(ct_info)
            else:
                grouped[ct.optgroup] = [ct_info]
        else:
            ungrouped.append(ct_info)
        choices.append(ct_info)

    return choices, grouped, ungrouped


def find_widget_class(name):

    for w_cls in get_all_widget_classes():
        if name.lower() in w_cls.__name__.lower():
            return w_cls
    return None


def get_htmltext_widget():
    '''Returns the default widget
    for html text fields
    '''

    return getattr(settings,
                   'LEONARDO_HTMLTEXT_WIDGET',
                   forms.Textarea
                   )


def render_region(widget=None, request=None, view=None,
                  page=None, region=None):
    """returns rendered content
    this is not too clear and little tricky,
    because external apps needs calling process method
    """

    # change the request
    if not isinstance(request, dict):
        request.query_string = None
        request.method = "GET"

    if not hasattr(request, '_feincms_extra_context'):
        request._feincms_extra_context = {}

    leonardo_page = widget.parent if widget else page
    render_region = widget.region if widget else region

    # call processors
    for fn in reversed(list(leonardo_page.request_processors.values())):
        try:
            r = fn(leonardo_page, request)
        except:
            pass

    contents = {}

    for content in leonardo_page.content.all_of_type(tuple(
            leonardo_page._feincms_content_types_with_process)):

        try:
            r = content.process(request, view=view)
        except:
            pass
        else:
            # this is HttpResponse object or string
            if not isinstance(r, six.string_types):
                r.render()
                contents[content.fe_identifier] = getattr(r, 'content', r)
            else:
                contents[content.fe_identifier] = r

    from leonardo.templatetags.leonardo_tags import _render_content

    region_content = ''.join(
        contents[content.fe_identifier] if content.fe_identifier in contents else _render_content(
            content, request=request, context={})
        for content in getattr(leonardo_page.content, render_region))

    return region_content
