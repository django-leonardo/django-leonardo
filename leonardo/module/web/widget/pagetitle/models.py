
from django.utils.translation import ugettext_lazy as _
from leonardo.module.web.models import Widget


class PageTitleWidget(Widget):

    class Meta:
        abstract = True
        verbose_name = _("page title")
        verbose_name_plural = _('page titles')

    def get_template_data(self, request):
        page = self.parent

        try:
            fragments = request._feincms_fragments
        except:
            fragments = {}

        title = fragments.get("_page_title", None)
        subtitle = fragments.get("_page_subtitle", None)

        return {
            'page': page,
            'title': title,
            'subtitle': subtitle,
        }
