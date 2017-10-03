from django.utils.functional import cached_property

from . import (
    get_default_pdf_model_cleaner_class,
    get_default_pdf_renderer_class,
)


class ModelToPDFHandler(object):
    pdf_model_cleaner_class = get_default_pdf_model_cleaner_class()
    pdf_renderer_class = get_default_pdf_renderer_class()

    def __init__(self, *args, **kwargs):
        if 'buffer' not in kwargs:
            raise ValueError('"buffer" is required.')

        if 'object' not in kwargs:
            raise ValueError('"object" is required.')

        if 'pdf_fields' not in kwargs:
            raise ValueError('"pdf_fields" is required.')

        self.buffer = kwargs.pop('buffer')
        self.object = kwargs.pop('object')
        self.pdf_fields = kwargs.pop('pdf_fields')
        self.context = kwargs.pop('context', {})

        if not isinstance(self.context, dict):
            raise TypeError('"context" has to be a dictionary.')

        self.kwargs = kwargs

    def get_pdf_fields(self):
        return self.pdf_fields

    def get_context(self):
        return self.context

    def get_object(self):
        return self.object

    def get_buffer(self):
        return self.buffer

    # Clean

    @cached_property
    def _pdf_model_cleaner_instance(self):
        klass = self.get_pdf_model_cleaner_class()

        return klass(self.get_object(),
                     self.get_pdf_fields(),
                     self.get_context())

    def get_pdf_model_cleaner_class(self):
        return self.pdf_model_cleaner_class

    def get_pdf_model_cleaner(self):
        return self._pdf_model_cleaner_instance

    def clean_pdf_fields(self):
        cleaner = self.get_pdf_model_cleaner()

        return cleaner.clean()

    # Render

    @cached_property
    def _pdf_renderer_instance(self):
        klass = self.get_pdf_renderer_class()

        return klass(self.get_buffer())

    def get_pdf_renderer_class(self):
        return self.pdf_renderer_class

    def get_pdf_renderer(self):
        return self._pdf_renderer_instance

    def render(self):
        # Clean fields
        cleaned_pdf_field_values = [x[1] for x in self.clean_pdf_fields()]

        # Render cleaned fields
        renderer = self.get_pdf_renderer()

        for field_bound_value in cleaned_pdf_field_values:
            renderer.render_field(field_bound_value)

        # Save renderered PDF to the buffer
        renderer.save()

        return self.buffer
