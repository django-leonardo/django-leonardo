from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from .dynamic import DynamicModelChoiceField


class SiteSelectField(DynamicModelChoiceField):

    def __init__(self, *args, **kwargs):

        super(SiteSelectField, self).__init__(
            label=_("Site"),
            queryset=Site.objects.all(),
            search_fields=('name', 'domain'),
            cls_name='sites.Site',
            empty_label='---',
            *args, **kwargs)
