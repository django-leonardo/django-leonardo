
from django.contrib import admin
from feincms.module.page.admin import PageAdmin as FeinPageAdmin
from feincms.module.page.models import Page
from reversion.admin import VersionAdmin

admin.site.unregister(Page)


class PageAdmin(FeinPageAdmin, VersionAdmin):

    pass

admin.site.register(Page, PageAdmin)
