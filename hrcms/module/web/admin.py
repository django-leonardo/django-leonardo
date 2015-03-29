
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


class PageAdmin(FeinPageAdmin):
    test = None

webcms_admin.register(Page, PageAdmin)
webcms_admin.register(User, UserAdmin)
webcms_admin.register(Site, SiteAdmin)
webcms_admin.register(Redirect, RedirectAdmin)
