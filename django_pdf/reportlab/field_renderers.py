from reportlab.platypus import Image, Paragraph

from django_pdf import pdf_fields
from django_pdf.pdf_fields import HTMLPDFField
from django_pdf.exceptions import PDFFieldRendererError
from django_pdf.renderers import AbstractPDFFieldRenderer
from django_pdf.utils import flatten_list


class ReportLabCharPDFFieldRenderer(AbstractPDFFieldRenderer):
    field_type = pdf_fields.CharPDFField

    def render(self, pdf_renderer, field_bound_value, context=None):
        reportlab_paragraph = Paragraph(field_bound_value.value,
                                        style=pdf_renderer.styles['Normal'])

        pdf_renderer._doc_elements.append(reportlab_paragraph)


class ReportLabTitlePDFFieldRenderer(AbstractPDFFieldRenderer):
    field_type = pdf_fields.TitlePDFField

    def render(self, pdf_renderer, field_bound_value, context=None):
        reportlab_paragraph = Paragraph(field_bound_value.value,
                                        style=pdf_renderer.styles['Title'])

        pdf_renderer._doc_elements.append(reportlab_paragraph)


class ReportLabHeadingPDFFieldRenderer(AbstractPDFFieldRenderer):
    field_type = pdf_fields.HeadingPDFField

    def render(self, pdf_renderer, field_bound_value, context=None):
        style_name = 'Heading{}'.format(field_bound_value.field.heading_level)

        reportlab_paragraph = Paragraph(
            field_bound_value.value,
            style=pdf_renderer.styles.get(style_name, 'Heading1')
        )

        pdf_renderer._doc_elements.append(reportlab_paragraph)


class ReportLabImagePDFFieldRenderer(AbstractPDFFieldRenderer):
    field_type = pdf_fields.ImagePDFField

    def render(self, pdf_renderer, field_bound_value, context=None):
        reportlab_image = Image(field_bound_value.value.open())

        pdf_renderer._doc_elements.append(reportlab_image)


class ReportLabHTMLPDFFieldRenderer(AbstractPDFFieldRenderer):
    field_type = HTMLPDFField

    def render(self, pdf_renderer, field_bound_value, context=None):
        self.render_parent_html_node(pdf_renderer, field_bound_value.value,
                                     context)

    def render_parent_html_node(self, pdf_renderer, node, context):
        """
        Render the top level HTML node.
        """
        # List of HTML tags
        if isinstance(node, HTMLPDFField.ElementList):
            for node_item in node:
                self.render_parent_html_node(pdf_renderer, node_item, context)
            return
        # Paragraph and text
        if isinstance(node, (HTMLPDFField.Paragraph,
                             HTMLPDFField.Text,
                             HTMLPDFField.Anchor,
                             HTMLPDFField.BoldText,
                             HTMLPDFField.ItalicText,
                             HTMLPDFField.UnderlinedText,
                             HTMLPDFField.StrikeThroughText,
                             HTMLPDFField.NewLine)):
            self.render_paragraph(pdf_renderer, node)
            return
        error_msg = "{} is not configured for this renderer."
        raise PDFFieldRendererError(error_msg.format(type(node).__name__))

    def convert_html_node_to_rlab_xml(self, element):
        if isinstance(element, HTMLPDFField.Paragraph):
            return [self.convert_html_node_to_rlab_xml(element.value)]
        if isinstance(element, HTMLPDFField.ElementList):
            items = []
            for list_item in element:
                items.append(self.convert_html_node_to_rlab_xml(list_item))
            return items
        if isinstance(element, HTMLPDFField.Text):
            return [self.convert_html_node_to_rlab_xml(element.value)]
        if isinstance(element, HTMLPDFField.NewLine):
            return ['<br />']
        if isinstance(element, HTMLPDFField.Anchor):
            return ['<link href="{}">{}</link>'.format(
                element.get_url(),
                ''.join(flatten_list(
                    self.convert_html_node_to_rlab_xml(element.value)
                ))
            )]
        if isinstance(element, HTMLPDFField.BoldText):
            content = self.convert_html_node_to_rlab_xml(element.value)
            return ['<b>{}</b>'.format(''.join(flatten_list(content)))]
        if isinstance(element, HTMLPDFField.ItalicText):
            content = self.convert_html_node_to_rlab_xml(element.value)
            return ['<i>{}</i>'.format(''.join(flatten_list(content)))]
        if isinstance(element, HTMLPDFField.UnderlinedText):
            content = self.convert_html_node_to_rlab_xml(element.value)
            return ['<u>{}</u>'.format(''.join(flatten_list(content)))]
        if isinstance(element, HTMLPDFField.StrikeThroughText):
            content = self.convert_html_node_to_rlab_xml(element.value)
            return ['<strike>{}</strike>'.format(''.join(
                flatten_list(content)
            ))]
        if isinstance(element, str):
            return [element]
        error_msg = "{} cannot be converted to ReportLab XML."
        raise PDFFieldRendererError(error_msg.format(type(element)))

    def render_paragraph(self, pdf_renderer, node):
        content = flatten_list(self.convert_html_node_to_rlab_xml(node))
        new_paragraph = Paragraph(
            ''.join(content),
            style=pdf_renderer.styles['Normal']
        )
        pdf_renderer._doc_elements.append(new_paragraph)
