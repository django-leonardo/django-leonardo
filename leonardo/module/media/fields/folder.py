
import os

from django.conf import settings
from django_select2.fields import AutoSelect2TagField
from django_select2.views import NO_ERR_RESP

from ..models import Folder
from .utils import FileField, FileMultipleField, FOLDER_SEARCH_FIELDS


class DirectorySelectField(AutoSelect2TagField):

    """returns list of plugins from github group or pypi

    it's simple PoC !
    """

    search_fields = ['tag__icontains', ]

    def get_field_values(self, value):
        return {'tag': value}

    def get_results(self, request, term, page, context):

        media_path = os.path.join(settings.MEDIA_ROOT)

        res = [
            (
                subdir,
                subdir,
                {}
            )
            for subdir in os.walk(media_path).next()[1]
        ]

        return NO_ERR_RESP, False, res


class FolderField(FileField):
    queryset = Folder.objects
    search_fields = FOLDER_SEARCH_FIELDS


class FolderMultipleField(FileMultipleField):
    queryset = Folder.objects
    search_fields = FOLDER_SEARCH_FIELDS
