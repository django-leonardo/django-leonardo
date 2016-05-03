

try:
    from .consumers import update_widget
    CHANNELS = True
except ImportError:
    CHANNELS = False


def update_widget_reciever(sender, instance, created, **kwargs):

    pass
#    if hasattr(instance, 'fe_identifier'):
#
#        update_widget(instance)

#    else:
#
#        # check related widgets
#
#        links = [rel.get_accessor_name()
#                 for rel in sender._meta.get_all_related_objects()]
#
#        for link in links:
#
#            if 'widget' in link:
#
#                for widget in getattr(instance, link).all():
#                    update_widget(widget)
#
