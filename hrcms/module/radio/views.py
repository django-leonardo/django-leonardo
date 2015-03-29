from django.template.loader import render_to_string
from django.http import HttpResponse
from django.db.models import loading

from webcms.utils.widgets import get_widget_from_id

def streamplayer_external_config(request, object_id, service_type):
    res = object_id.split('-')
    model_cls = loading.get_model(res[1], res[2])
    obj = model_cls.objects.get(parent=res[3], id=res[4])

    data = render_to_string('widget/streamplayer/%s-config.xml' % service_type, {
        'widget': obj,
        'request': request,
    })
    
    response = HttpResponse(data, mimetype='text/xml')
    return response
