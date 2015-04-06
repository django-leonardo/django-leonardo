# -*- coding: UTF-8 -*-
"""
Business admin.
"""

from django.contrib import admin
from webcms.models import webcms_admin
from models import Entity

def address(object):
    output = u"%s<br />%s %s" % (object.street, object.zip_code, object.city)
    return output
address.short_description = u'address'
address.allow_tags = True

class EntityAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'business_id', 'email', 'phone', address, 'bank_account')
    list_filter = ('role',)

admin.site.register(Entity, EntityAdmin)
webcms_admin.register(Entity, EntityAdmin)
