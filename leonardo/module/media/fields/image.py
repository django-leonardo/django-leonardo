from ..models import Image
from .utils import FileField, FileMultipleField


class ImageField(FileField):
    queryset = Image.objects


class ImageMultipleField(FileMultipleField):
    queryset = Image.objects
