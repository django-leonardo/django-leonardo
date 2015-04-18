from __future__ import absolute_import, unicode_literals

import logging
import sys
import traceback

from django import template
from django.conf import settings
from django.db.models.loading import get_model
from django.http import HttpRequest

from feincms import settings as feincms_settings
from feincms.module.page.extensions.navigation import PagePretender
from feincms.utils.templatetags import (
    SimpleNodeWithVarAndArgs,
    do_simple_node_with_var_and_args_helper,
    SimpleAssignmentNodeWithVarAndArgs,
    do_simple_assignment_node_with_var_and_args_helper)


from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


from .models import Page

def page_xml_list(request, object_id=None):
    if object_id == None:
        object_list = Page.objects.filter(parent=None)
    else:
        obj = Page.objects.get(pk=object_id)
        object_list = Page.objects.filter(parent=obj)

    data = render_to_string('web/page_list.xml', {
        'object_list': object_list,
        'request': request,
    })

    response = HttpResponse(data, mimetype='text/xml')
    return response

def page_xml_detail(request, object_id):
    obj = Page.objects.get(pk=object_id)

    data = render_to_string('web/page_detail.xml', {
        'object': obj,
        'request': request,
    })
    
    response = HttpResponse(data, mimetype='text/xml')
    return response

def page_print_detail(request, object_id):
    feincms_page = Page.objects.get(id=object_id)

    level=1
    depth=1
    group=None

    page_class = _get_page_model()

    if feincms_page is None:
        return []

    if isinstance(feincms_page, HttpRequest):
        try:
            feincms_page = page_class.objects.for_request(
                feincms_page, best_match=True)
        except page_class.DoesNotExist:
            return []

    mptt_opts = feincms_page._mptt_meta

    # mptt starts counting at zero
    mptt_level_range = [level - 1, level + depth - 1]

    queryset = feincms_page.__class__._default_manager.in_navigation().filter(
        **{
            '%s__gte' % mptt_opts.level_attr: mptt_level_range[0],
            '%s__lt' % mptt_opts.level_attr: mptt_level_range[1],
        }
    )

    page_level = getattr(feincms_page, mptt_opts.level_attr)

    # Used for subset filtering (level>1)
    parent = None

    if level > 1:
        # A subset of the pages is requested. Determine it depending
        # upon the passed page instance

        if level - 2 == page_level:
            # The requested pages start directly below the current page
            parent = feincms_page

        elif level - 2 < page_level:
            # The requested pages start somewhere higher up in the tree
            parent = feincms_page.get_ancestors()[level - 2]

        elif level - 1 > page_level:
            # The requested pages are grandchildren of the current page
            # (or even deeper in the tree). If we would continue processing,
            # this would result in pages from different subtrees being
            # returned directly adjacent to each other.
            queryset = page_class.objects.none()

        if parent:
            if getattr(parent, 'navigation_extension', None):
                # Special case for navigation extensions
                return list(parent.extended_navigation(
                    depth=depth, request=context.get('request')))

            # Apply descendant filter
            queryset &= parent.get_descendants()

    if depth > 1:
        # Filter out children with inactive parents
        # None (no parent) is always allowed
        parents = set([None])
        if parent:
            # Subset filtering; allow children of parent as well
            parents.add(parent.id)

        def _parentactive_filter(iterable):
            for elem in iterable:
                if elem.parent_id in parents:
                    yield elem
                parents.add(elem.id)

        queryset = _parentactive_filter(queryset)

    if hasattr(feincms_page, 'navigation_extension'):
        # Filter out children of nodes which have a navigation extension
        def _navext_filter(iterable):
            current_navextension_node = None
            for elem in iterable:
                # Eliminate all subitems of last processed nav extension
                if current_navextension_node is not None and \
                   current_navextension_node.is_ancestor_of(elem):
                    continue

                yield elem
                if getattr(elem, 'navigation_extension', None):
                    current_navextension_node = elem
                    try:
                        for extended in elem.extended_navigation(
                                depth=depth, request=context.get('request')):
                            # Only return items from the extended navigation
                            # which are inside the requested level+depth
                            # values. The "-1" accounts for the differences in
                            # MPTT and navigation level counting
                            this_level = getattr(
                                extended, mptt_opts.level_attr, 0)
                            if this_level < level + depth - 1:
                                yield extended
                    except Exception as e:
                        logger.warn(
                            "feincms_nav caught exception in navigation"
                            " extension for page %d: %s",
                            current_navextension_node.id, format_exception(e))
                else:
                    current_navextension_node = None

        queryset = _navext_filter(queryset)

    if group is not None:
        # navigationgroups extension support
        def _navigationgroup_filter(iterable):
            for elem in iterable:
                if getattr(elem, 'navigation_group', None) == group:
                    yield elem

        queryset = _navigationgroup_filter(queryset)

    # Return a list, not a generator so that it can be consumed
    # several times in a template.
    return list(queryset)
