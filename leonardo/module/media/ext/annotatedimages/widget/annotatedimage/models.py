# -#- coding: utf-8 -#-

import datetime
from decimal import Decimal
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.template.context import RequestContext

from webcms.models import Widget
from webcms.module.media.ext.annotatedimages.models import AnnotatedImage 

class AnnotatedImageWidget(Widget):
    image = models.ForeignKey(AnnotatedImage, verbose_name=_("image"), blank=True, null=True)
    show_info = models.BooleanField(verbose_name=_("show info"), default=False)
    width = models.IntegerField(verbose_name=_("width"), default=720)
    height = models.IntegerField(verbose_name=_("height"), default=480, blank=True, null=True)

    def get_size(self):
        return u"%sx%s" % (self.width, self.height)

    def render_content(self, options):
        annotations = []
        hundred = Decimal('100.00')
        width = Decimal(self.width)
        height = Decimal(self.height)
        if self.image:
            for annotation in self.image.annotations.filter(active=True).order_by('number'):
                data = {
                    'obj': annotation,
                    'top': str(annotation.top / hundred * self.height).split('.')[0],
                    'left': str(annotation.left / hundred * self.width).split('.')[0],
                }
                if annotation.width:
                    data['width'] = str(annotation.width / hundred * self.width).split('.')[0]

                if annotation.height:
                    data['height'] = str(annotation.height / hundred * self.height).split('.')[0]

                annotations.append(data)

        context = RequestContext(options.get('request'), { 
            'widget': self,
            'annotations': annotations,
        })

        return render_to_string(self.template_name, context)

    class Meta:
        abstract = True
        verbose_name = _("annotated image")
        verbose_name_plural = _('annotated images')