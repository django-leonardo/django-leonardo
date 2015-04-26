
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from filer.admin import FolderAdmin
from filer.models import Folder
from filer.models.imagemodels import Image as FilerImage

from .models import *

#from filer.admin.fileadmin import FileAdmin
#from filer.admin.imageadmin import ImageAdmin as BaseImageAdmin



class ImageAdmin(ModelAdmin):

    list_display = ('__str__', 'name')


class DocumentAdmin(ModelAdmin):

    pass


class VideoAdmin(ModelAdmin):

    pass

class FileAdmin(ModelAdmin):

    pass

class FolderAdmin(ModelAdmin):

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


class MyFolderAdmin(FolderAdmin):
    pass

#admin.site.unregister(Folder)
#admin.site.register(Folder, FolderAdmin)
#admin.site.register(File, FileAdmin)
#admin.site.unregister(File)

admin.site.register(Image, ImageAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Video, VideoAdmin)
