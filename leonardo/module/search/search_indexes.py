from haystack import indexes, fields
from leonardo.module.web.models import Page


class PageIndex(indexes.SearchIndex, indexes.Indexable):

    """
    Index for FeinCMS Page objects

    Body is generated using a complex template which includes rendered content
    for many content objects
    """

    url = fields.CharField(model_attr="_cached_url")
    text = fields.CharField(document=True, use_template=True)

    title = fields.CharField(model_attr="title")
    slug = fields.CharField(model_attr="slug")
    page_title = fields.CharField(model_attr="_page_title")
    meta_description = fields.CharField(model_attr="meta_description")
    meta_keywords = fields.CharField(model_attr="meta_keywords")
    content_title = fields.CharField(model_attr="_content_title")
    content = fields.CharField(model_attr="content")

    creation_date = fields.DateTimeField(model_attr='creation_date', null=True)
    modification_date = fields.DateTimeField(model_attr='modification_date', null=True)

    def should_update(self, instance, **kwargs):
        return instance.is_active()

    def get_model(self):
        return Page

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(active=True)

    def get_updated_field(self):
        return "modification_date"
