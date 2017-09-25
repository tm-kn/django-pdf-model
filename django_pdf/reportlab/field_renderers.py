from reportlab.platypus import Paragraph

from django_pdf.renderers import PDFFieldRenderer
from django_pdf.pdf_fields import CharPDFField


class ReportLabCharPDFFieldRenderer(PDFFieldRenderer):
    acceptable_field_types = [
        CharPDFField
    ]

    def render(self, pdf_renderer, field_bound_value):
        reportlab_paragraph = Paragraph(field_bound_value.value,
                                        style=pdf_renderer._styles['Normal'])

        pdf_renderer._doc_elements.append(reportlab_paragraph)
