from django.conf.urls.defaults import *

urlpatterns = patterns('webcms.module.media.views',
    url(r'^scan-files/$', 'scan_files', name="webcms_media_scan_files"),
    url(r'^create-folder/$', 'create_folder', name="webcms_media_create_folder"),
    url(r'^upload-files/$', 'select_folder', name="webcms_media_select_folder"),
    url(r'^upload-files/(?P<folder_id>[0-9]+)/$', 'upload_files', name="webcms_media_upload_files"),
    url(r'^upload-files/(?P<folder_id>[0-9]+)/process/$', 'upload_files_process', name="webcms_media_upload_files_process"),
)
