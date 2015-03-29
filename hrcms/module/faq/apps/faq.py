from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('webcms.module.glossary.views',
    url(r'^$', 'term_list', name='webcms_glosary_index'),
)
