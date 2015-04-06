from django.contrib import admin
from django.contrib import messages

from django.views.decorators.http import require_http_methods
from django.http import Http404
from django.conf.urls.defaults import patterns, url
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.contenttypes import generic
from models import SVGFile, SVGComposerFile

class SVGFileAdmin(admin.ModelAdmin):
    list_display = ['name']
    
    def get_urls(self):
        urls = super(SVGFileAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^(\d+)/overwrite/$', 
                self.admin_site.admin_view(self.overwrite),
                name='%s_%s_overwrite'% (self.model._meta.app_label, 
                                      self.model._meta.module_name),
             )
            )
        return my_urls + urls
    
    def overwrite(self, request, svgfile_id, **kwargs):
        if request.method == 'POST':
            if 'xml' in request.POST:
                svgfile = get_object_or_404(SVGFile,id=svgfile_id)
                messenger, message_text = svgfile.save_from_editor(request.POST['xml'])
                messenger(request, message_text)
                return render_to_response('admin/svgfile/overwrite_status.html',
                                          {'messages':messages.get_messages(request)})
        else:
            return Http404()

class SVGComposerFileAdmin(admin.ModelAdmin):
    list_display = ['name']
    
    def get_urls(self):
        urls = super(SVGComposerFileAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^(\d+)/overwrite/$', 
                self.admin_site.admin_view(self.overwrite),
                name='%s_%s_overwrite'% (self.model._meta.app_label, 
                                      self.model._meta.module_name),
             )
            )
        return my_urls + urls
    
    def overwrite(self, request, svgfile_id, **kwargs):
        if request.method == 'POST':
            if 'xml' in request.POST:
                svgfile = get_object_or_404(SVGComposerFile,id=svgfile_id)
                messenger, message_text = svgfile.save_from_editor(request.POST['xml'])
                messenger(request, message_text)
                return render_to_response('admin/svgfile/overwrite_status.html',
                                          {'messages':messages.get_messages(request)})
        else:
            return Http404()

admin.site.register(SVGFile, SVGFileAdmin)
admin.site.register(SVGComposerFile, SVGComposerFileAdmin)