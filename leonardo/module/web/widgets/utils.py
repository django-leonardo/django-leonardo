from django.db.models import loading


def get_widget_from_id(id):
    """returns widget object by id

    example web-htmltextwidget-2-2
    """

    res = id.split('-')
    try:
        model_cls = loading.get_model(res[0], res[1])
        obj = model_cls.objects.get(parent=res[2], id=res[3])
    except:
        obj = None
    return obj


def get_widget_class_from_id(id):
    """returns widget class by id

    example web-htmltextwidget-2-2
    """

    res = id.split('-')
    try:
        model_cls = loading.get_model(res[1], res[2])
    except:
        model_cls = None
    return model_cls
