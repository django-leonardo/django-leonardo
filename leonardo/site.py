
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.sites import AdminSite


class LeonardoAdminSite(AdminSite):

    site_header = getattr(settings, "SITE_HEADER", "Leonardo administration")

    site_title = getattr(settings, "SITE_TITLE", "Leonardo site admin")

    def get_urls(self):

        # connect all admin members

        self._registry.update(admin.site._registry)

        return super(LeonardoAdminSite, self).get_urls()

leonardo_admin = LeonardoAdminSite(name="admin")
