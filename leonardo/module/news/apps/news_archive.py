from django.conf.urls.defaults import *

urlpatterns = patterns('webcms.module.news.views',
    (r'^$', 'news_entry_list', {}, 'webcms_news_entry_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<object_slug>[^/]+)/$', 'elephantblog.views.entry', name='webcms_news_entry_detail'),
    (r'^(?P<object_slug>[\-\w]+)/$', 'news_entry_detail', {'year':None,'month':None,'day':None}, 'webcms_news_entry_dated_detail'),
)
