from haystack import indexes, fields
from .models import File, Image, Document, Video


class FileIndex(indexes.SearchIndex, indexes.Indexable):

    """
    Index for File objects

    """

    text = fields.CharField(document=True, use_template=True)
    url = fields.CharField(model_attr="url")

    title = fields.CharField(model_attr="name", null=True)
    description = fields.CharField(model_attr="description", null=True)
    folder = fields.CharField(model_attr="folder", null=True)
    original_filename = fields.CharField(model_attr="original_filename", null=True)

    uploaded_at = fields.DateTimeField(model_attr='uploaded_at', null=True)

    def get_model(self):
        return File

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_public=True)

    def get_updated_field(self):
        return "uploaded_at"


class ImageIndex(FileIndex):

    def get_model(self):
        return Image


class DocumentIndex(FileIndex):

    def get_model(self):
        return Document


class VideoIndex(FileIndex):

    def get_model(self):
        return Video
