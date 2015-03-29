# -*- coding: UTF-8 -*-

from django.conf import settings
from django.conf.urls.defaults import *

from feincms.translations import short_language_code

from elephantblog.models import Entry
from elephantblog.feeds import EntryFeed

entry_dict = {
    'paginate_by' : 10,
}

urlpatterns = patterns('',
    url(r'^headlines/$', 'elephantblog.views.entry_list', dict(entry_dict, template_name='blog/entry_headlines.html'), name='webcms_blog_headlines'),
    url(r'^feed/$', EntryFeed()),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[^/]+)/$', 'elephantblog.views.entry', name='webcms_blog_entry_detail'),
    url(r'^category/(?P<category>[^/]+)/$', 'elephantblog.views.entry_list', name='webcms_blog_category_list'),
    url(r'^(category/(?P<category>[^/]+)/)?((?P<year>\d{4})/)?((?P<month>\d{2})/)?((?P<day>\d{2})/)?$', 'elephantblog.views.entry_list', entry_dict, name='webcms_blog_list'),
)

#if 'tagging' in settings.INSTALLED_APPS:
#    urlpatterns += patterns('',url(r'^tag/(?P<tag>[^/]+)/$', 'tagging.views.tagged_object_list', { 'template_name':'blog/entry_list_tagged.html', 'paginate_by':entry_dict['paginate_by']}, name='webcms_blog_tag'),
#)

