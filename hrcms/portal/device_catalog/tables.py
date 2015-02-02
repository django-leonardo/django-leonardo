from django.conf import settings
from django.core import urlresolvers
from django.template.defaultfilters import timesince
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _

from horizon import tables




class DeviceTable(tables.DataTable):

    id = tables.Column('id', verbose_name=_("ID"), hidden=True)
    verbose_name = tables.Column('name', verbose_name=_("Verbose Name"))
    description = tables.Column('model_device', verbose_name=_("Model Device"))

    def get_object_id(self, datum):
        return str(datum['name'])

    def get_object_display(self, datum):
        return str(datum['name'])

    class Meta:
        name = "devices"
        verbose_name = _("Devices")