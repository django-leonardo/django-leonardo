from django.contrib import admin

from .models import NewsEntry, NewsEntryAdmin

admin.site.register(NewsEntry, NewsEntryAdmin)
