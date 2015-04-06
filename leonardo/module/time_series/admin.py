from django.contrib import admin

from django.utils.translation import ugettext_lazy as _

from boardie.module.time_series.models import TimeSeriesSource

class TimeSeriesSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'data']

admin.site.register(TimeSeriesSource, TimeSeriesSourceAdmin)
