from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django.utils.functional import cached_property

from . import get_default_model_to_pdf_handler_class
from .models import PDFModelMixin


class PDFModelSingleObjectMixin(SingleObjectMixin):
    PDF_FIELDS_ATTRIBUTE_NAME = 'pdf_field_list'
    pdf_to_model_handler_class = get_default_model_to_pdf_handler_class()

    @classmethod
    def get_pdf_fields(cls):
        if hasattr(cls, cls.PDF_FIELDS_ATTRIBUTE_NAME):
            return getattr(cls, cls.PDF_FIELDS_ATTRIBUTE_NAME)

        if issubclass(cls.model, PDFModelMixin):
            return cls.model.get_pdf_fields()

        error_msg = '{view_class} has to have "{attr_name}" specified or ' \
                    'take PDFModelMixin instance as a model.'

        raise NotImplementedError(error_msg.format(
            view_class=cls.__name__,
            attr_name=cls.PDF_FIELDS_ATTRIBUTE_NAME
        ))

    @cached_property
    def _pdf_response(self):
        return HttpResponse(content_type='application/pdf')

    def get_pdf_response(self):
        return self._pdf_response

    def get_pdf_context(self):
        return {
            'request': self.request
        }

    def render_pdf(self):
        handler = self.get_pdf_to_model_handler()

        return handler.render()

    @cached_property
    def _pdf_to_model_handler_instance(self):
        klass = self.get_pdf_to_model_handler_class()

        return klass(buffer=self.get_pdf_response(),
                     object=self.get_object(),
                     pdf_fields=self.get_pdf_fields(),
                     context=self.get_pdf_context())

    def get_pdf_to_model_handler_class(self):
        return self.pdf_to_model_handler_class

    def get_pdf_to_model_handler(self):
        return self._pdf_to_model_handler_instance


class PDFModelView(PDFModelSingleObjectMixin, View):
    def get(self, request, *args, **kwargs):
        return self.render_pdf()
