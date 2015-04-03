
from django.contrib import admin
from feincms.module.page.modeladmins import PageAdmin as FeinPageAdmin
from hrcms.models import Page
from reversion.admin import VersionAdmin


class PageAdmin(FeinPageAdmin, VersionAdmin):

    pass

admin.site.register(Page, PageAdmin)
