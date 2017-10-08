from django.test import TestCase

from django_pdf.pdf_fields import HTMLPDFField


class TestHTMLPDFField(TestCase):
    def setUp(self):
        self.html_field = HTMLPDFField('some_name')

    def test_simple_paragraph(self):
        cleaned_value = self.html_field.clean("""
            <p>
                Lorem Ipsum
            </p>
        """)
        # Cleaning a field returns a list with only paragraph inside it
        self.assertIsInstance(cleaned_value, HTMLPDFField.ElementList)
        self.assertEqual(len(cleaned_value), 1)
        paragraph = cleaned_value[0]
        self.assertIsInstance(paragraph, HTMLPDFField.Paragraph)
        # Paragaph should contain a list with a text object
        paragraph_value = paragraph.value
        self.assertIsInstance(paragraph_value, HTMLPDFField.ElementList)
        self.assertEqual(len(paragraph_value), 1)
        text = paragraph_value[0]
        self.assertIsInstance(text, HTMLPDFField.Text)
        # Text object should contain string
        text_value = text.value
        self.assertIsInstance(text_value, str)
        self.assertEqual(text_value, 'Lorem Ipsum')
