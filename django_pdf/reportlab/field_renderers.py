from reportlab.platypus import Image, Paragraph

from django_pdf import pdf_fields
from django_pdf.renderers import PDFFieldRenderer


class ReportLabCharPDFFieldRenderer(PDFFieldRenderer):
    field_type = pdf_fields.CharPDFField

    def render(self, pdf_renderer, field_bound_value):
        reportlab_paragraph = Paragraph(field_bound_value.value,
                                        style=pdf_renderer.styles['Normal'])

        pdf_renderer._doc_elements.append(reportlab_paragraph)


class ReportLabTitlePDFFieldRenderer(PDFFieldRenderer):
    field_type = pdf_fields.TitlePDFField

    def render(self, pdf_renderer, field_bound_value):
        reportlab_paragraph = Paragraph(field_bound_value.value,
                                        style=pdf_renderer.styles['Title'])

        pdf_renderer._doc_elements.append(reportlab_paragraph)


class ReportLabHeadingPDFFieldRenderer(PDFFieldRenderer):
    field_type = pdf_fields.HeadingPDFField

    def render(self, pdf_renderer, field_bound_value):
        style_name = 'Heading{}'.format(field_bound_value.field.heading_level)

        reportlab_paragraph = Paragraph(
            field_bound_value.value,
            style=pdf_renderer.styles.get(style_name, 'Heading1')
        )

        pdf_renderer._doc_elements.append(reportlab_paragraph)


class ReportLabImagePDFFieldRenderer(PDFFieldRenderer):
    field_type = pdf_fields.ImagePDFField

    def render(self, pdf_renderer, field_bound_value):
        reportlab_image = Image(field_bound_value.open())

        pdf_renderer._doc_elements.append(reportlab_image)
