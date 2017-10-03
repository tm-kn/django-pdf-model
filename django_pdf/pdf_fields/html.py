from bs4 import BeautifulSoup

from . import PDFField


class HTMLPDFFieldCompoundValue(object):
    def __init__(self, value1, value2):
        self.values = (value1, value2)


class HTMLPDFFieldElement(object):
    pass


class HTMLPDFFieldParagraph(HTMLPDFFieldElement):
    pass


class HTMLPDFFieldUnorderedList(HTMLPDFFieldElement):
    pass


class HTMLPDFFieldOrderedList(HTMLPDFFieldElement):
    pass


class HTMLPDFFieldAnchor(HTMLPDFFieldElement):
    pass


class HtmlPDFFieldImage(HTMLPDFFieldElement):
    pass


class HtmlPDFFieldBoldText(HTMLPDFFieldElement):
    pass


class HtmlPDFFieldItalicText(HTMLPDFFieldElement):
    pass


class HtmlPDFFieldUnderlinedText(HTMLPDFFieldElement):
    pass


class HtmlPDFFieldStrikeThroughText(HTMLPDFFieldElement):
    pass


class HTMLPDFField(PDFField):
    ALLOWED_VALUE_TYPES = [
        str
    ]

    def clean_value(self, value, context=None):
        soup = BeautifulSoup(value, 'html5lib')

        paragraph = HTMLPDFFieldParagraph(str(soup))

        return HTMLPDFFieldCompoundValue(paragraph, None)
