from inspect import isclass

from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django.utils.functional import cached_property

from . import get_default_pdf_renderer_class
from .cleaner import PDFModelCleaner
from .models import PDFModelMixin
from .renderers import PDFRenderer


class PDFModelSingleObjectMixin(SingleObjectMixin):
    PDF_FIELDS_ATTRIBUTE_NAME = 'pdf_field_list'
    PDF_RENDERER_CLASS_ATTRIBUTE_NAME = 'pdf_renderer_class'

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
    def pdf_renderer(self):
        return self._get_pdf_renderer()

    @cached_property
    def pdf_response(self):
        return HttpResponse(content_type='application/pdf')

    @cached_property
    def pdf_model_cleaner_class(self):
        return self._get_pdf_model_cleaner_class()

    @cached_property
    def pdf_model_cleaner(self):
        return self._get_pdf_model_cleaner()

    def get_pdf_context(self):
        return {
            'request': self.request
        }

    def get_pdf_renderer_class(self):
        # Get PDF Renderer set on the view
        view_value = self._get_view_pdf_renderer_class()

        if view_value:
            return view_value

        # Fallback to the PDF renderer set on the model
        model_value = self._get_model_pdf_renderer_class()

        if model_value:
            return model_value

        # Fallback to the default setting set in the project
        # settings
        return get_default_pdf_renderer_class()

    def _get_model_pdf_renderer_class(self):
        model_value = self.get_object().get_pdf_renderer_class()

        if model_value and not (isclass(model_value)
                                or issubclass(model_value, PDFRenderer)):
            raise TypeError("\"pdf_renderer_class\" on {} has to be a "
                            "PDFRedenderer instance, not {}.".format(
                                    self.model.__class__.__name__,
                                    type(model_value).__name__
                            ))
        return model_value

    def _get_view_pdf_renderer_class(self):
        if hasattr(self, self.PDF_RENDERER_CLASS_ATTRIBUTE_NAME):
            view_value = getattr(self, self.PDF_RENDERER_CLASS_ATTRIBUTE_NAME)

            if view_value and not (isclass(view_value)
                                   or issubclass(view_value, PDFRenderer)):
                raise TypeError("\"pdf_renderer_class\" on {} has to be a "
                                "PDFRedenderer instance, not {}.".format(
                                    self.__class__.__name__,
                                    type(view_value).__name__
                                ))

            return view_value

    def _get_pdf_renderer(self):
        renderer_class = self.get_pdf_renderer_class()
        return renderer_class(self.pdf_response)

    def _get_pdf_model_cleaner_class(self):
        return PDFModelCleaner

    def _get_pdf_model_cleaner(self):
        return self.pdf_model_cleaner_class(self.get_object(),
                                            self.get_pdf_fields(),
                                            self.get_pdf_context())

    def _render_pdf_fields(self):
        for field_bound_value in self._clean_pdf_fields().values():
            self.pdf_renderer.render_field(field_bound_value)

        self.pdf_renderer.save()

    def _clean_pdf_fields(self):
        return self.pdf_model_cleaner.clean()

    def write_pdf_to_response(self):
        self._render_pdf_fields()


class PDFModelView(PDFModelSingleObjectMixin, View):
    def get(self, request, *args, **kwargs):
        self.write_pdf_to_response()

        return self.pdf_response
