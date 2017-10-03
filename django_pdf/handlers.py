from django.utils.functional import cached_property


class ModelToPDFHandler(object):
    cleaner = None
    pdf_renderer_class = None

    @cached_property
    def pdf_renderer_instance(self):
        self.get_pdf_renderer_class()()

    def get_context(self):
        return self.context

    def get_pdf_renderer_class(self):
        return self.pdf_renderer_class

    def get_pdf_renderer(self):
        return self.pdf_renderer_instance
