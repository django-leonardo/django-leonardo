from collections import defaultdict
from django.conf import settings
from django.core import urlresolvers
from django.template.defaultfilters import timesince
from django.utils.http import urlencode
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _

from horizon import tables

from .client import robotice_client

def get_image_categories(item, metrics):

    categories = []

    for m in metrics:
        for metric in item["metrics"]:
            if metric == m:
                categories.append(metric["key"])
    return categories


class ItemsFilter(tables.FixedFilterAction):

    def get_fixed_buttons(self):
        def make_dict(text, tenant, icon):
            return dict(text=text, value=tenant, icon=icon)

        self.metrics = robotice_client.metrics.list({})
        buttons = []
        for metric in self.metrics:
            buttons.append(make_dict(_(metric["name"]), metric["key"], 'fa fa-arrow-up'))
        return buttons

    def categorize(self, table, items):
        tenants = defaultdict(list)
        for item in items:
            categories = get_image_categories(item, self.metrics)
            for category in categories:
                tenants[category].append(item)
        return tenants

class UpdateRow(tables.Row):
    ajax = False

    def load_cells(self, image=None):
        super(UpdateRow, self).load_cells(image)
        # Tag the row with the image category for client-side filtering.
        image = self.datum
        self.metrics = robotice_client.metrics.list({})
        image_categories = get_image_categories(image, self.metrics)
        for category in image_categories:
            self.classes.append('category-' + category) 

class PreviewAction(tables.LinkAction):
    verbose_name = "Preview"
    name = "preview_action"
    success_url = "horizon:portal:device_catalog:index"
    url = "horizon:portal:device_catalog:preview"

    classes = ("ajax-modal",)

    def get_link_url(self, datum):
        return urlresolvers.reverse(self.url, args=[datum["id"]])

class DetailAction(tables.LinkAction):
    verbose_name = "Detail"
    name = "detail_action"
    success_url = "horizon:portal:device_catalog:index"
    url = "horizon:portal:device_catalog:detail"
    classes = ("ajax-modal",)

    def get_link_url(self, datum):
        return urlresolvers.reverse(self.url, args=[datum["id"]])

class DeviceTable(tables.DataTable):

    id = tables.Column('id', verbose_name=_("ID"), hidden=True)
    name = tables.Column('name',
        verbose_name=_("Device Name"),
        link=(lambda x: reverse("horizon:portal:device_catalog:detail", args=[x["id"]])))
    metrics = tables.Column('metrics', verbose_name=_("Metrics"), filters=(lambda x: ", ".join([metric["name"] for metric in x]),))
    related = tables.Column('related', verbose_name=_("Related devices"), filters=(lambda x: ", ".join([metric["name"] for metric in x]),))
    required = tables.Column('required', verbose_name=_("Required devices"), filters=(lambda x: ", ".join([metric["name"] for metric in x]),))

    def get_object_id(self, datum):
        return str(datum['name'])

    def get_object_display(self, datum):
        return str(datum['name'])

    class Meta:
        name = "devices"
        verbose_name = _("Devices")
        row_class = UpdateRow
        row_actions = (PreviewAction,)
        table_actions = (ItemsFilter,)