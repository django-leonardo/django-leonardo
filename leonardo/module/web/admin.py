
from django.contrib import admin
from feincms.module.page.modeladmins import PageAdmin as FeinPageAdmin
from .models import Page


class PageAdmin(FeinPageAdmin):

    pass

admin.site.register(Page, PageAdmin)
