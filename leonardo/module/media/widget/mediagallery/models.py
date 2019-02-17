# -#- coding: utf-8 -#-

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from leonardo.module.media.fields.folder import FolderField
from leonardo.module.web.models import ListWidget
from leonardo.module.web.widgets.forms import WidgetUpdateForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from leonardo.module.media.models import Image
from constance import config


DETAIL_CHOICES = (
    ('open_modal', _('open in modal window')),
    ('open_new_window', _('open new window')),
    ('on_page', _('disply in page')),
)

SIZE_CHOICES = (
    ('small', _('small')),
    ('medium', _('medium')),
    ('large', _('large')),
)


class FolderForm(WidgetUpdateForm):

    folder = FolderField()


class MediaGalleryWidget(ListWidget):

    feincms_item_editor_form = FolderForm

    icon = "fa fa-picture-o"

    folder = models.ForeignKey('media.Folder', verbose_name=_(
        "Directory"), related_name="%(app_label)s_%(class)s_folders")
    size = models.CharField(max_length=255, verbose_name=_(
        "thumbnail size"), choices=SIZE_CHOICES, default='small')
    detail = models.CharField(max_length=255, verbose_name=_(
        "detail view"), choices=DETAIL_CHOICES, default='modal')

    def get_items(self):
        return self.folder.media_file_files.instance_of(Image)

    def get_size(self):
        if not hasattr(self, '_image_size'):
            self._image_size = getattr(
                settings,
                'MEDIA_THUMB_%s_GEOM' % self.size.upper(),
                '96x96')

        return self._image_size

    def get_directories(self, request):
        """Return directories
        """

        queryset = self.folder.media_folder_children.all().order_by(*config.MEDIA_FOLDERS_ORDER_BY.split(","))

        paginator = Paginator(queryset, self.objects_per_page)

        page = request.GET.get('page', None)

        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:

            if page == "all":
                object_list = queryset
            else:
                object_list = paginator.page(1)

        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)

        return object_list

    def get_template_data(self, request, *args, **kwargs):
        '''Add image dimensions'''

        # little tricky with vertical centering
        dimension = int(self.get_size().split('x')[0])

        data = {}

        if dimension <= 356:
            data['image_dimension'] = "row-md-13"

        if self.get_template_name().name.split("/")[-1] == "directories.html":
            data['directories'] = self.get_directories(request)

        return data

    class Meta:
        abstract = True
        verbose_name = _("media gallery")
        verbose_name_plural = _('media galleries')
