
from django.contrib import admin

from webcms.module.banners.models import Banner, Slot
from webcms.models import webcms_admin

class Banner_Inline(admin.TabularInline):
    model = Banner

class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'slot', '__unicode__', 'is_published', 'ordering', 'destination', )
    list_display_links = ('id', '__unicode__',)
    list_filter = ('is_published', 'slot', )
    list_editable = ('ordering',)
    search_fields = ('id', '__unicode__', )

class SlotAdmin(admin.ModelAdmin):
    inlines = [Banner_Inline]
    list_display = ('name',)

admin.site.register(Banner, BannerAdmin)
admin.site.register(Slot, SlotAdmin)

webcms_admin.register(Banner, BannerAdmin)
webcms_admin.register(Slot, SlotAdmin)
