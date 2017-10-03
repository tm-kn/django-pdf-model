from django.utils.module_loading import import_string

from . import settings


def get_default_pdf_renderer_class_string():
    return settings.PDF_RENDERER_CLASS


def get_default_pdf_renderer_class():
    return import_string(get_default_pdf_renderer_class_string())


def get_default_pdf_model_cleaner_class_string():
    return settings.PDF_MODEL_CLEANER_CLASS


def get_default_pdf_model_cleaner_class():
    return import_string(get_default_pdf_model_cleaner_class_string())


def get_default_model_to_pdf_handler_class_string():
    return settings.MODEL_TO_PDF_HANDLER_CLASS


def get_default_model_to_pdf_handler_class():
    return import_string(get_default_model_to_pdf_handler_class_string())
