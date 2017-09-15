from django.core import checks
from django.db import models
from django.utils.module_loading import import_string


class PDFModelMixin(models.Model):
    PDF_MODEL_VIEW_PATH = '{}.views.PDFModelView'.format(__package__)
    PDF_FIELDS_ATTRIBUTE_NAME = 'pdf_field_list'
    PDF_RENDERER_CLASS_ATTRIBUTE_NAME = 'pdf_renderer_class'

    cached_pdf_file = models.FileField(editable=False, blank=True, null=True)

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def get_pdf_view_class(cls):
        klass = import_string(cls.PDF_MODEL_VIEW_PATH)

        return type('{}{}'.format(cls.__name__, klass.__name__),
                    (klass,), dict(model=cls))

    @classmethod
    def as_pdf_view(cls, **kwargs):
        return cls.get_pdf_view_class().as_view(**kwargs)

    @classmethod
    def get_pdf_fields(cls):
        if not hasattr(cls, cls.PDF_FIELDS_ATTRIBUTE_NAME):
            return None

        return getattr(cls, cls.PDF_FIELDS_ATTRIBUTE_NAME)

    def get_pdf_renderer_class(self):
        if not hasattr(self, self.PDF_RENDERER_CLASS_ATTRIBUTE_NAME):
            return None

        return getattr(self, self.PDF_RENDERER_CLASS_ATTRIBUTE_NAME)

    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(cls._check_pdf_fields())

        return errors

    @classmethod
    def _check_pdf_fields(cls):
        if not cls.get_pdf_fields():
            message = '{model} has to specify {pdf_fields_attribute} ' \
                      'because it subclasses PDFModelMixin.'

            yield checks.Error(
                message.format(
                    model=cls.__name__,
                    pdf_fields_attribute=cls.__PDF_FIELDS_ATTRIBUTE_NAME
                ),
                obj=cls.__name__
            )
