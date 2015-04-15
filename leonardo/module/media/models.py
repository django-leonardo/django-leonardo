
from datetime import datetime
import os
from django.db import models
from filer.models.filemodels import File
from filer.models.abstract import BaseImage
from django.utils.translation import ugettext_lazy as _

from filer import settings as filer_settings  # noqa


class Document(File):

    @classmethod
    def matches_file_type(cls, iname, ifile, request):
        # the extensions we'll recognise for this file type
        # (majklk): TODO move to settings or live config
        filename_extensions = ['.pdf', '.xls', ]
        ext = os.path.splitext(iname)[1].lower()
        return ext in filename_extensions

    class Meta:
        verbose_name = ("document")
        verbose_name_plural = ('documents')


class Video(File):

    @classmethod
    def matches_file_type(cls, iname, ifile, request):
        filename_extensions = ['.dv', '.mov', '.mp4', '.avi', '.wmv', ]
        ext = os.path.splitext(iname)[1].lower()
        return ext in filename_extensions

    class Meta:
        verbose_name = ("video")
        verbose_name_plural = ('videos')


class Image(BaseImage):

    date_taken = models.DateTimeField(_('date taken'), null=True, blank=True,
                                      editable=False)

    author = models.CharField(
        _('author'), max_length=255, null=True, blank=True)

    must_always_publish_author_credit = models.BooleanField(
        _('must always publish author credit'), default=False)
    must_always_publish_copyright = models.BooleanField(
        _('must always publish copyright'), default=False)

    @classmethod
    def matches_file_type(cls, iname, ifile, request):
        filename_extensions = ['.jpg', '.png', '.jpeg', ]
        ext = os.path.splitext(iname)[1].lower()
        return ext in filename_extensions

    def save(self, *args, **kwargs):
        if self.date_taken is None:
            try:
                exif_date = self.exif.get('DateTimeOriginal', None)
                if exif_date is not None:
                    d, t = exif_date.split(" ")
                    year, month, day = d.split(':')
                    hour, minute, second = t.split(':')
                    if getattr(settings, "USE_TZ", False):
                        tz = get_current_timezone()
                        self.date_taken = make_aware(datetime(
                            int(year), int(month), int(day),
                            int(hour), int(minute), int(second)), tz)
                    else:
                        self.date_taken = datetime(
                            int(year), int(month), int(day),
                            int(hour), int(minute), int(second))
            except Exception:
                pass
        if self.date_taken is None:
            self.date_taken = now()
        super(Image, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _('images')

        # You must define a meta with en explicit app_label
        app_label = 'media'
