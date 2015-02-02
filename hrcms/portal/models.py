
from feincms.module.page.extensions.navigation import NavigationExtension, PagePretender

from feincms.module.page.models import Page

from feincms.content.application.models import app_reverse

#app_reverse('index', 'hrcms.portal.urls', args=[])

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy

from django.utils.translation import ugettext_lazy as _
from feincms.content.application.models import ApplicationContent
from feincms.module.page.models import Page
from feincms.content.richtext.models import RichTextContent
from feincms.content.medialibrary.models import MediaFileContent


class PortalExtension(NavigationExtension):
    name = 'portal'

    def children(self, page, **kwargs):
        yield PagePretender(
                title="Supported Devices",
                url=reverse("horizon:portal:device_catalog:index"),
                )

Page.register_extensions('feincms.module.page.extensions.navigation')