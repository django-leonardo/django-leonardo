
from leonardo.module.web.models import Widget
from leonardo.module.nav.mixins import NavigationWidgetMixin


class NavigationWidget(Widget, NavigationWidgetMixin):

    """Base class for navigation widget
    """

    class Meta:
        abstract = True

"""
class MediaCategoriesNavigationExtension(NavigationExtension):
    name = _('')

    def children(self, page, **kwargs):
        base_url = page.get_absolute_url()
        category_list = Folder.objects.filter(parent=None)
        for category in category_list:
            subchildren = []
            for subcategory in category.media_folder_children.all():
                subchildren.append(PagePretender(
                    title=subcategory,
                    url='%s%s/%s/' % (base_url, category.name, subcategory.name),
                    level=5
                ))
            yield PagePretender(
                title=category,
                url='%s%s/' % (base_url, category.name),
                children=subchildren,
                level=5
            )
"""