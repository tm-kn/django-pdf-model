from django.core.files.images import ImageFile

from . import AbstractPDFField


class ImagePDFField(AbstractPDFField):
    ALLOWED_VALUE_TYPES = [
        ImageFile
    ]

    def clean_value(self, value, context=None):
        return value
