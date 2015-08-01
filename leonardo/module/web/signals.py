
import django.dispatch
from dbtemplates.conf import settings
from dbtemplates.models import Template

try:
    from django.utils.timezone import now
except ImportError:
    from datetime import datetime
    now = datetime.now


def dbtemplate_save(sender, instance, created, **kwargs):
    """create widget/page content/base theme from given db template::
        /widget/icon/my_awesome.html
        /base/widget/my_new_widget_box.html
        /base/page/my_new_page_layout.html
    """

    if created:
        if 'widget' in instance.name:
            name = instance.name.split('/')[-1]
            kwargs = {
                'name': name.split('.')[0],
                'label': name.split('.')[0].capitalize(),
                'template': instance,
            }
            if 'base/widget' in instance.name:
                from leonardo.module.web.models import WidgetBaseTheme
                theme_cls = WidgetBaseTheme
            else:
                from leonardo.module.web.models import WidgetContentTheme
                theme_cls = WidgetContentTheme
                from leonardo.utils.widgets import find_widget_class
                w_cls_name = instance.name.split('/')[-2]
                w_cls = find_widget_class(w_cls_name)
                if w_cls is None:
                    raise Exception('widget class for %s not found' % w_cls_name)
                kwargs['widget_class'] = w_cls.__name__
            theme_cls(**kwargs).save()

        if 'base/page' in instance.name:
            from leonardo.module.web.models import PageTheme
            page_theme = PageTheme()
            page_theme.label = '{} layout'.format(
                instance.name.split("/")[-1].split('.')[0].title())
            page_theme.name = instance.name.split("/")[-1]
            page_theme.template = instance
            page_theme.save()

template_post_save = django.dispatch.Signal(providing_args=["instance", "created"])
template_post_save.connect(dbtemplate_save, dispatch_uid="sync_themes")


def save(self, *args, **kwargs):
    self.last_changed = now()
    # If content is empty look for a template with the given name and
    # populate the template instance with its content.
    if settings.DBTEMPLATES_AUTO_POPULATE_CONTENT and not self.content:
        self.populate()

    sync_themes = kwargs.pop('sync_themes', True)
    created = True
    if self.pk:
        created = False

    super(Template, self).save(*args, **kwargs)

    if sync_themes:
        from leonardo.module.web.signals import template_post_save
        template_post_save.send(
            sender=self.__class__, instance=self, created=created)
