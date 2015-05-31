
import six
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from horizon_contrib.common import get_class

from ..models import (Page, PageColorScheme, PageTheme, WidgetBaseTheme,
                      WidgetContentTheme, WidgetDimension)

from .bootstrap_example import BOOTSTRAP


def create_new_site(run_syncall=False, with_user=True, request=None):
    """returns page with some widgets
    """

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
                    'parent': page,
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

    # generic stuff
    for cls_name, cls_attrs in six.iteritems(BOOTSTRAP):

        cls = get_class(cls_name)

        instance, created = cls.objects.get_or_create(**cls_attrs)

    return root_page
