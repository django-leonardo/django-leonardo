
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
#from filer.admin.fileadmin import FileAdmin
#from filer.admin.imageadmin import ImageAdmin as BaseImageAdmin
from filer.models.imagemodels import Image as FilerImage

from .models import *


class ImageAdmin(ModelAdmin):

    list_display = ('__str__', 'name')


class DocumentAdmin(ModelAdmin):

    pass


class VideoAdmin(ModelAdmin):

    pass


try:
    from oscar.apps.promotions.models import Image as OscarImage
    admin.site.unregister(OscarImage)
except Exception:
    pass

try:
    admin.site.unregister(FilerImage)
except Exception:
    pass

admin.site.register(Image, ImageAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Video, VideoAdmin)
