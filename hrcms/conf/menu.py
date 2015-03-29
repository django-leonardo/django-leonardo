# -#- coding: utf-8 -#-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.menu import items, Menu

from hrcms.module.web.conf.admin import menu_options, web_options, conf_options, web_menu
from hrcms.module.eshop.conf.admin import store_options
#from hrcms.module.folio.conf.admin import folio_options

common_options = [
    items.MenuItem(_('Web site'), '/', description=_('Basic web components and applications.'), children=web_options),
    items.MenuItem(_('Electronic store'), '/', description=_('Complete electronic store management and utilities.'), children=store_options),
#    items.MenuItem(_('Professional portfolio'), reverse('webcms_admin:folio_project_changelist'), description=_('Management of electronic portfolio module.'), children=folio_options),
    items.MenuItem(_('Advanced settings'), '/', description=_('Advanced settings, analytics and maintenance tools.'), children=conf_options),
]

class AdminDashboard(Menu):
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.template = 'admin/dashboard.html'
        self.children = common_options

    def init_with_context(self, context):
        return super(AdminDashboard, self).init_with_context(context)

class AdminMenu(Menu):
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.template = 'admin/site_menu.html'
        self.children = menu_options + common_options

    def init_with_context(self, context):
        return super(AdminMenu, self).init_with_context(context)