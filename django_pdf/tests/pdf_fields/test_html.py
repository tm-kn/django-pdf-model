from django.test import TestCase

from django_pdf.pdf_fields import HTMLPDFField
from django_pdf.exceptions import PDFFieldCleaningError


class TestHTMLPDFField(TestCase):
    def setUp(self):
        self.html_field = HTMLPDFField('some_name')

    def test_field_name(self):
        self.assertEqual(self.html_field.name, 'some_name')

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

    def test_image(self):
        cleaned_value = self.html_field.clean("""
            <img src="image.jpg">
        """)
        self.assertEqual(len(cleaned_value), 1)
        image = cleaned_value[0]
        self.assertIsInstance(image, HTMLPDFField.Image)
        self.assertEqual(image.attrs['src'], 'image.jpg')

    def test_image_without_src(self):
        cleaned_value = self.html_field.clean("""
            <img>
        """)
        # If no argument is passed, src will be none
        self.assertEqual(len(cleaned_value), 1)
        self.assertIsNone(cleaned_value[0].attrs['src'])

    def test_image_with_empty_src(self):
        cleaned_value = self.html_field.clean("""
            <img src="">
        """)
        # If no argument is passed, src will be an empty string
        self.assertEqual(len(cleaned_value), 1)
        self.assertIsInstance(cleaned_value[0].attrs['src'], str)
        self.assertEqual(cleaned_value[0].attrs['src'], '')


class TestHTMLPDFFieldImage(TestCase):
    def test_image_without_src(self):
        with self.assertRaises(PDFFieldCleaningError) as cm:
            HTMLPDFField.Image(None)
        exception_message = str(cm.exception)
        self.assertIn('src', exception_message)
        self.assertIn('HTMLPDFFieldImage', exception_message)

    def test_image_with_src(self):
        image = HTMLPDFField.Image(None, attrs={'src': 'http://dgg.gg'})
        self.assertEqual(image.attrs['src'], 'http://dgg.gg')


class TestHTMLPDFElementList(TestCase):
    def setUp(self):
        self.html_list = HTMLPDFField.ElementList()

    def test_repr_empty(self):
        self.assertEqual(repr(self.html_list), 'HTMLPDFFieldElementList([])')

    def test_adding_value_in_init(self):
        paragraph = HTMLPDFField.Paragraph(HTMLPDFField.Text('test'))
        html_list = HTMLPDFField.ElementList(paragraph)
        self.assertEqual(len(html_list), 1)
        self.assertEqual(html_list[0], paragraph)

    def test_adding_multiple_values_in_init(self):
        paragraph = HTMLPDFField.Paragraph(HTMLPDFField.Text('test'))
        image = HTMLPDFField.Image(None, attrs={'src': 'image.jpg'})
        html_list = HTMLPDFField.ElementList(paragraph, image)
        self.assertEqual(len(html_list), 2)
        self.assertEqual(html_list[0], paragraph)
        self.assertEqual(html_list[1], image)

    def test_appending_wrong_type(self):
        with self.assertRaises(TypeError):
            self.html_list.append('abc')

        with self.assertRaises(TypeError):
            self.html_list.append(None)

        with self.assertRaises(TypeError):
            self.html_list.append(123)

    def test_append(self):
        self.html_list.append(HTMLPDFField.Paragraph(
            HTMLPDFField.Text('test')
        ))
        self.assertEqual(len(self.html_list), 1)


class TestHTMLPDFFieldAnchor(TestCase):
    def test_empty_href(self):
        with self.assertRaises(PDFFieldCleaningError) as cm:
            HTMLPDFField.Anchor(None)
        exception_message = str(cm.exception)
        self.assertIn('href', exception_message)
        self.assertIn('HTMLPDFFieldAnchor', exception_message)
