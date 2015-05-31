
from django.contrib import admin

from .clipboardadmin import ClipboardAdmin
from .fileadmin import FileAdmin
from .folderadmin import FolderAdmin
from .imageadmin import ImageAdmin
from .permissionadmin import PermissionAdmin
from ..models import File, FolderPermission, Folder, Clipboard, Image


admin.site.register(File, FileAdmin)
admin.site.register(Folder, FolderAdmin)
admin.site.register(Clipboard, ClipboardAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(FolderPermission, PermissionAdmin)

from ..models import Document, Video, Vector
# common stuff
from .mediaadmin import DocumentAdmin, VectorAdmin, VideoAdmin

admin.site.register(Video, VideoAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Vector, VectorAdmin)
