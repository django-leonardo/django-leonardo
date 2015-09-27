
from django.conf import settings
from django.utils import six


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
    return widgets


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
