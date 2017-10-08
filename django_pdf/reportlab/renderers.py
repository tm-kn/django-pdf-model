from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate

from django_pdf.renderers import AbstractPDFRenderer

from . import field_renderers


class SimpleDocTemplateReportLabPDFRenderer(AbstractPDFRenderer):
    _doc_elements = []

    field_renderers = [
        field_renderers.ReportLabCharPDFFieldRenderer,
        field_renderers.ReportLabTitlePDFFieldRenderer,
        field_renderers.ReportLabHeadingPDFFieldRenderer,
        field_renderers.ReportLabHTMLPDFFieldRenderer,
    ]

    def set_up(self):
        self._doc = SimpleDocTemplate(self.buffer_object)
        self._styles = getSampleStyleSheet()

    @property
    def styles(self):
        return self._styles

    def save(self):
        self._doc.build(self._doc_elements)
