from django.contrib import admin

from webcms.models import webcms_admin
from models import NewsEntry, NewsEntryAdmin

admin.site.register(NewsEntry, NewsEntryAdmin)
webcms_admin.register(NewsEntry, NewsEntryAdmin)
