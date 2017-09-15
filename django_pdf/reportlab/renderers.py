from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph

from ..renderers import PDFRenderer


class SimpleDocTemplateReportLabPDFRenderer(PDFRenderer):
    _doc_elements = []

    def set_up(self):
        self._doc = SimpleDocTemplate(self.buffer_object)
        self._styles = getSampleStyleSheet()

    def render_field(self, field_bound_value):
        # TODO: Implement rendering fields
        paragraph = Paragraph(field_bound_value.value,
                              style=self._styles['Normal'])

        self._doc_elements.append(paragraph)

    def save(self):
        self._doc.build(self._doc_elements)
