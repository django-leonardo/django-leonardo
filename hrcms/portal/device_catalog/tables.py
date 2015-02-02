from django.conf import settings
from django.core import urlresolvers
from django.template.defaultfilters import timesince
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _

from horizon import tables


class PreviewAction(tables.LinkAction):
    verbose_name = "Preview"
    name = "preview_action"
    success_url = "horizon:portal:device_catalog:index"
    url = "horizon:portal:device_catalog:detail"

    classes = ("ajax-modal",)

    def get_link_url(self, datum):
        return urlresolvers.reverse(self.url, args=[datum["id"]])

class DetailAction(tables.LinkAction):
    verbose_name = "Detail"
    name = "detail_action"
    success_url = "horizon:portal:device_catalog:index"
    url = "horizon:portal:device_catalog:detail"

    def get_link_url(self, datum):
        return urlresolvers.reverse(self.url, args=[datum["id"]])

class DeviceTable(tables.DataTable):

    id = tables.Column('id', verbose_name=_("ID"), hidden=True)
    name = tables.Column('name', verbose_name=_("Device Name"))
    metrics = tables.Column('metrics', verbose_name=_("Metrics"), filters=(lambda x: ", ".join([metric["name"] for metric in x]),))

    def get_object_id(self, datum):
        return str(datum['name'])

    def get_object_display(self, datum):
        return str(datum['name'])

    class Meta:
        name = "devices"
        verbose_name = _("Devices")
        row_actions = (PreviewAction,)