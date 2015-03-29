from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from admin_tools.menu import items

web_options = []

try:
    web_options.append(items.MenuItem(_('Pages'), reverse('webcms_admin:page_page_changelist'), description=_('Manage site structure and content widgets.')))
except:
    pass

try:
    web_options.append(items.MenuItem(_('Files'), reverse('webcms_admin:media_file_changelist'), description=_('All multimedial files uploaded to the site.')))
except:
    pass

try:
    web_options.append(items.MenuItem(_('Media categories'), reverse('webcms_admin:media_category_changelist'), description=_('Multimedial categories to be used in other modules.')))
except:
    pass

try:
    web_options.append(items.MenuItem(_('News'), reverse('webcms_admin:news_newsentry_changelist'), description=_('Periodical short messages ordered in timely manner.')))
except:
    pass

try:
    web_options.append(items.MenuItem(_('Links'), reverse('webcms_admin:links_link_changelist'), description=_('Links to the other pages or resources.')))
except:
    pass

try:
    web_options.append(items.MenuItem(_('Link lists'), reverse('webcms_admin:links_linkcategory_changelist'), description=_('Lists of links.')))
except:
    pass

try:
    web_options.append(items.MenuItem(_('Banners'), reverse('webcms_admin:banners_banner_changelist'), description=_('Easy management of banners.')))
except:
    pass

try:
    web_options.append(items.MenuItem(_('Banner slots'), reverse('webcms_admin:banners_bannerslot_changelist'), description=_('Easy management of multiple banner positions.')))
except:
    pass

try:
    web_options.append(items.MenuItem(_('Glossary terms'), reverse('webcms_admin:glossary_term_changelist'), description=_('List of terms with synonims.')))
except:
    pass

try:
    web_options.append(items.MenuItem(_('Image annotations'), reverse('webcms_admin:annotatedimages_imageannotation_changelist'), description=_('List of terms with synonims.')))
except:
    pass

try:
    web_options.append(items.MenuItem(_('Annotated images'), reverse('webcms_admin:annotatedimages_annotatedimage_changelist'), description=_('List of terms with synonims.')))
except:
    pass

try:
    web_options.append(items.MenuItem(_('FAQ categories'), reverse('webcms_admin:faq_faqcategory_changelist')))
except:
    pass

try:
    web_options.append(items.MenuItem(_('Frequest questions'), reverse('webcms_admin:faq_faq_changelist')))
except:
    pass

try:
    web_options.append(items.MenuItem(_('Flexible forms'), reverse('webcms_admin:form_designer_form_changelist')))
except:
    pass

try:
    web_options.append(items.MenuItem(_('Form submissions'), reverse('webcms_admin:form_designer_formsubmission_changelist')))
except:
    pass

web_menu = items.MenuItem(_('Web site'), '/', description=_('Basic web components and applications.'), children=web_options),

conf_options = [
    items.MenuItem(_('Users'), '/', description=_('Administration of system users.')),
#    items.MenuItem(_('Analytics'), reverse('webcms_admin:analytics')),
    items.MenuItem(_('Site setup'), '/'),
]

conf_menu = items.MenuItem(_('Advanced settings'), '/', description=_('Advanced settings, analytics and maintenance tools.'), children=conf_options),

menu_options = [
    items.MenuItem(_('Project dashboard'), '/', description=_('Project admin dashboard.')),
#    items.Bookmarks(),
]
