from leonardo.module.web.widgets.forms import WidgetUpdateForm
from leonardo.module.media.fields.image import ImageField


class SiteHeadingForm(WidgetUpdateForm):

    logo = ImageField(required=False)
