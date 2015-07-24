

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
                'name': name,
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
