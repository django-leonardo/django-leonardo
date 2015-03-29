from django.contrib import admin

from django.utils.translation import ugettext_lazy as _

from hrcms.module.graph.models import GraphSource

class GraphSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'data']

admin.site.register(GraphSource, GraphSourceAdmin)
