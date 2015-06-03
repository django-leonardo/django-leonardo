
import os
import six
import logging
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from horizon_contrib.common import get_class

from ..models import (Page, PageColorScheme, PageTheme, WidgetBaseTheme,
                      WidgetContentTheme, WidgetDimension)

from .bootstrap_example import BOOTSTRAP

LOG = logging.getLogger('leonardo')


def get_loaded_scripts(directory=getattr(settings, 'LEONARDO_BOOTSTRAP_DIR')):
    """return dictionary of loaded scripts from specified directory
    """

    scripts = {}

    for root, dirnames, filenames in os.walk(directory):

        for file_name in filenames:

            try:

                ext = file_name.split('.')[1]

                with open(os.path.join(directory, file_name), 'r') as file:

                    if ext in ['yaml', 'yml']:
                        import yaml
                        scripts[file_name] = yaml.load(file)
                    elif ext == 'json':
                        import json
                        scripts[file_name] = json.load(file)

            except Exception as e:
                LOG.exception('Error in during loading {} file'.format(file_name))

    return scripts


def _handle_regions(regions, feincms_object):

    for region, widgets in six.iteritems(regions):
        for widget_cls, widget_attrs in six.iteritems(widgets):

            try:
                WidgetCls = get_class(widget_cls)
            except Exception as e:
                raise Exception('Cannout load {} with {}'.format(
                    widget_cls, e))

            # TODO create form and validate options
            w_attrs = widget_attrs.get('attrs', {})
            w_attrs.update({
                'parent': feincms_object,
                'region': region,
                'ordering': 0
            })

            w_attrs['content_theme'] = WidgetContentTheme.objects.get(
                name=w_attrs['content_theme'],
                widget_class=WidgetCls.__name__)
            w_attrs['base_theme'] = WidgetBaseTheme.objects.get(
                name=w_attrs['base_theme'])
            widget = WidgetCls(**w_attrs)
            widget.save(created=False)

            for size, width in six.iteritems(
                    widget_attrs.get('dimenssions', {})):

                WidgetDimension(**{
                    'widget_id': widget.pk,
                    'widget_type': widget.content_type,
                    'size': size,
                    'width': width
                }).save()


def create_new_site(run_syncall=False, with_user=True, request=None,
                    script='demo.yaml'):
    """load all available scripts and try scaffold new site from them

    TODO(majklk): refactor and support for more cases

    """

    if run_syncall:
        from django.core import management
        management.call_command('sync_all', force=True)

    try:
        scripts = get_loaded_scripts()
        BOOTSTRAP = scripts[script]
    except KeyError:
        raise Exception('Cannot find {} in {}'.format(script, scripts))

    root_page = None

    for username, user_attrs in six.iteritems(BOOTSTRAP.pop('auth.User', {})):

        # create and login user
        if with_user and not User.objects.exists():
            User.objects.create_superuser(
                username, user_attrs['mail'], user_attrs['password'])

            # login
            if request:
                auth_user = authenticate(
                    username=username, password=user_attrs['password'])
                login(request, auth_user)

    for page_name, page_attrs in six.iteritems(BOOTSTRAP.pop('web.Page', {})):

        page_theme_name = page_attrs.pop('theme', '__first__')
        page_color_scheme_name = page_attrs.pop('color_scheme', '__first__')

        regions = page_attrs.pop('content', {})

        try:
            if page_theme_name == '__first__':
                theme = PageTheme.objects.first()
            else:
                theme = PageTheme.objects.get(name=page_theme_name)
        except Exception:
            raise Exception("You havent any themes \
                please install someone and run sync_all")
        else:
            page_attrs['theme'] = theme

        try:
            if page_color_scheme_name == '__first__':
                color_scheme = PageColorScheme.objects.first()
            else:
                color_scheme = PageColorScheme.objects.get(
                    name=page_color_scheme_name)
        except Exception:
            raise Exception("You havent any themes \
                please install someone and run sync_all")
        else:
            page_attrs['color_scheme'] = color_scheme

        page, created = Page.objects.get_or_create(**page_attrs)

        # TODO from attrs etc..
        root_page = page

        _handle_regions(regions, page)

    # generic stuff
    for cls_name, entries in six.iteritems(BOOTSTRAP):

        for entry, cls_attrs in six.iteritems(entries):

            cls = get_class(cls_name)

            regions = cls_attrs.pop('content', {})

            # load FK from
            # author: {'pk': 1, 'type': 'auth.User'}
            for attr, value in six.iteritems(cls_attrs):
                if isinstance(value, dict):
                    cls_type = value.get('type', None)
                    if cls_type:
                        try:
                            cls_attrs[attr] = get_class(
                                cls_type).objects.get(pk=value.get('pk'))
                        except Exception as e:
                            raise Exception(
                                'Cannot load FK {} not Found original exception {}'.format(cls_type, e))

            instance, created = cls.objects.get_or_create(**cls_attrs)

            _handle_regions(regions, instance)

    return root_page
