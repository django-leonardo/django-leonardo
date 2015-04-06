
from django.contrib import admin
from django.contrib.admin.sites import AdminSite


class LeonardoAdminSite(AdminSite):

    def get_urls(self):

        # connect all admin members

        self._registry.update(admin.site._registry)

        return super(LeonardoAdminSite, self).get_urls()

leonardo_admin = LeonardoAdminSite(name="admin")
