from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate

from django_pdf.renderers import PDFRenderer

from . import field_renderers


class SimpleDocTemplateReportLabPDFRenderer(PDFRenderer):
    _doc_elements = []

    field_renderers = [
        field_renderers.ReportLabCharPDFFieldRenderer,
        field_renderers.ReportLabTitlePDFFieldRenderer,
        field_renderers.ReportLabHeadingPDFFieldRenderer,
    ]

    def set_up(self):
        self._doc = SimpleDocTemplate(self.buffer_object)
        self._styles = getSampleStyleSheet()

    @property
    def styles(self):
        return self._styles

    def save(self):
        self._doc.build(self._doc_elements)
