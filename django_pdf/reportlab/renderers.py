from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate

from django_pdf.pdf_fields import CharPDFField
from django_pdf.renderers import PDFRenderer

from .field_renderers import ReportLabCharPDFFieldRenderer


class SimpleDocTemplateReportLabPDFRenderer(PDFRenderer):
    _doc_elements = []

    field_renderers = [
        (CharPDFField, ReportLabCharPDFFieldRenderer)
    ]

    def set_up(self):
        self._doc = SimpleDocTemplate(self.buffer_object)
        self._styles = getSampleStyleSheet()

    def save(self):
        self._doc.build(self._doc_elements)
