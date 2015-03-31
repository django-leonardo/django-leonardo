
from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.redirects.admin import RedirectAdmin
from django.contrib.redirects.models import Redirect
from django.contrib.sites.admin import SiteAdmin
from django.contrib.sites.models import Site
from feincms.module.page.admin import PageAdmin as FeinPageAdmin
from feincms.module.page.forms import PageAdminForm
from feincms.module.page.models import Page
from hrcms.models import webcms_admin
from reversion.admin import VersionAdmin

admin.site.unregister(Page)


class PageAdmin(FeinPageAdmin, VersionAdmin):
    test = None

admin.site.register(Page, PageAdmin)
#admin.site.register(User, UserAdmin)
#admin.site.register(Site, SiteAdmin)
#admin.site.register(Redirect, RedirectAdmin)
