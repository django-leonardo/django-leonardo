from django.contrib import admin

from webcms.models import webcms_admin
from models import Document, DocumentAdmin

admin.site.register(Document, DocumentAdmin)
webcms_admin.register(Document, DocumentAdmin)
