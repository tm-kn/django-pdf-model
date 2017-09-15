from django.utils.module_loading import import_string

from . import settings


def get_default_pdf_renderer_class_string():
    return settings.PDF_RENDERER_CLASS


def get_default_pdf_renderer_class():
    return import_string(get_default_pdf_renderer_class_string())
