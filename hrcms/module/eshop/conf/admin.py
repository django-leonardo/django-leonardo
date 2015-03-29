
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from admin_tools.menu import items

store_options = []

try:
    store_options.append(items.MenuItem(_('Orders'), reverse('webcms_store_admin_order_list')))
except:
    pass

try:
    store_options.append(items.MenuItem(_('Customers'), reverse('webcms_admin:contact_contact_changelist')))
except:
    pass

try:
    store_options.append(items.MenuItem(_('Catalog products'), reverse('webcms_admin:product_product_changelist')))
except:
    pass

try:
    store_options.append(items.MenuItem(_('Product lists'), reverse('webcms_admin:store_productlist_changelist')))
except:
    pass

if 'product.modules.configurable' in settings.INSTALLED_APPS:
    try:
        store_options.append(items.MenuItem(_('Option groups'), reverse('webcms_admin:product_optiongroup_changelist')))
    except:
        pass

try:
    store_options.append(items.MenuItem(_('Categories'), reverse('webcms_admin:product_category_changelist')))
except:
    pass

try:
    store_options.append(items.MenuItem(_('Brands'), reverse('webcms_admin:brand_brand_changelist')))
except:
    pass

if 'webcms.module.store.ext.manufacturer' in settings.INSTALLED_APPS:
    try:
        store_options.append(items.MenuItem(_('Manufacturers'), reverse('webcms_admin:manufacturer_manufacturer_changelist')))
    except:
        pass

try:
    store_options.append(items.MenuItem(_('Attribute options'), reverse('webcms_admin:product_attributeoption_changelist')))
except:
    pass

try:
    store_options.append(items.MenuItem(_('Branches'), reverse('webcms_admin:branch_branch_changelist')))
except:
    pass

try:
    store_options.append(items.MenuItem(_('Regions'), reverse('webcms_admin:branch_region_changelist')))
except:
    pass

try:
    store_options.append(items.MenuItem(_('Feeds'), reverse('webcms_admin:feed_feed_changelist')))
except:
    pass

try:
    store_options.append(items.MenuItem(_('Carriers'), reverse('webcms_admin:tiered_carrier_changelist')))
except:
    pass

try:
    store_options.append(items.MenuItem(_('Tax classes'), reverse('webcms_admin:product_taxclass_changelist')))
except:
    pass

try:
    store_options.append(items.MenuItem(_('Tax Rates'), reverse('webcms_admin:area_taxrate_changelist')))
except:
    pass

try:
    store_options.append(items.MenuItem(_('Price tiers'), reverse('webcms_admin:tieredpricing_pricingtier_changelist')))
except:
    pass

store_menu = items.MenuItem(_('Electronic store'), '/', description=_('Complete electronic store management and utilities.'), children=store_options),