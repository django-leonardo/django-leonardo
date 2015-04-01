
from django.contrib import admin
from django.contrib.admin.sites import AdminSite


class HRCMSAdminSite(AdminSite):

    def get_urls(self):

        # connect all admin members

        self._registry.update(admin.site._registry)

        return super(HRCMSAdminSite, self).get_urls()

hrcms_admin = HRCMSAdminSite(name="admin")

# support for old stuff
webcms_admin = hrcms_admin
