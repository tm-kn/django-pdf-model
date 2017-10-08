import logging

from bs4 import BeautifulSoup, NavigableString, Tag

from . import AbstractPDFField
from ..exceptions import HTMLPDFFieldElementNotFound

logger = logging.getLogger(__name__)


class HTMLPDFFieldElement(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.value)})"


class HTMLPDFFieldElementList(list):
    def __init__(self, *args):
        super().__init__()
        if args:
            self.append(args[0])

    def append(self, value):
        if not isinstance(value, HTMLPDFFieldElement):
            raise TypeError(f"{type(self).__name__} has to contain "
                            "HTMLPDFFieldElement objects only, "
                            "not {type(value)}.")
        super().append(value)

    def __repr__(self):
        return f"{type(self).__name__}({super().__repr__()})"


class HTMLPDFFieldText(HTMLPDFFieldElement):
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


class HtmlPDFFieldNewLine(HTMLPDFFieldElement):
    def __init__(self, *args):
        super().__init__(None)

    def __repr__(self):
        return f"{self.__class__.__name__}()"


class HTMLPDFField(AbstractPDFField):
    ALLOWED_VALUE_TYPES = [
        str
    ]
    Anchor = HTMLPDFFieldAnchor
    BoldText = HtmlPDFFieldBoldText
    Element = HTMLPDFFieldElement
    ElementList = HTMLPDFFieldElementList
    ItalicText = HtmlPDFFieldItalicText
    Paragraph = HTMLPDFFieldParagraph
    StrikeThroughText = HtmlPDFFieldStrikeThroughText
    Text = HTMLPDFFieldText
    UnderlinedText = HtmlPDFFieldUnderlinedText
    NewLine = HtmlPDFFieldNewLine
    HTML_TAG_MAPPINGS = {
        'p': Paragraph,
        'a': Anchor,
        'b': BoldText,
        'strong': BoldText,
        'u': UnderlinedText,
        'br': NewLine,
        ('del', 's', 'strike'): StrikeThroughText,
        ('i', 'em'): ItalicText,
        ('b', 'strong'): BoldText,
    }
    TRAVERSE_AND_IGNORE_TAGS = [
        'div',
    ]
    IGNORE_TAGS = [
        'iframe',
        'embed',
    ]

    def clean_value(self, value, context=None):
        return self.convert_html_to_pdf_field_structure(value)

    def convert_html_to_pdf_field_structure(self, value):
        soup = BeautifulSoup(value, 'html5lib')
        try:
            return self.traverse_html_tag(soup.body.contents)
        except HTMLPDFFieldElementNotFound:
            logger.exception("Could not find any HTML elements to generate "
                             "PDF content out of.")

    def convert_html_to_pdf_text(self, value):
        html_list = HTMLPDFFieldElementList()
        # Convert new line characters
        splitlined_string = value.strip().splitlines()
        for key, text_string in enumerate(splitlined_string):
            # Replace new lines
            if key < len(splitlined_string) and key > 0:
                html_list.append(self.NewLine())
            # Make sure we're not adding empty strings full of
            # whitespaces.
            text_string = text_string.strip()
            if text_string:
                html_list.append(self.Text(text_string))
        return html_list

    def get_pdf_field_element_for_tag(self, tag_name):
        for key, element_class in self.HTML_TAG_MAPPINGS.items():
            if isinstance(key, tuple):
                if tag_name in [x.lower() for x in key]:
                    return element_class
                continue
            if key.lower() == tag_name.lower():
                return element_class
        raise KeyError

    def traverse_list(self, tags_list):
        structure = HTMLPDFFieldElementList()
        for child in tags_list:
            try:
                structure += self.traverse_html_tag(child)
            except HTMLPDFFieldElementNotFound:
                logger.exception('Could not generate PDF content out of the '
                                 'HTML content.')
        return structure

    def traverse_html_tag(self, tag):
        # If it's a list, evaluate its children and append
        if isinstance(tag, list):
            return self.traverse_list(tag)
        # Convert strings to PDF field text object.
        if isinstance(tag, NavigableString):
            return self.convert_html_to_pdf_text(str(tag))
        # Convert tag to a PDF field type and evaluate its children.
        if isinstance(tag, Tag):
            try:
                klass = self.get_pdf_field_element_for_tag(tag.name)
            except KeyError:
                if tag.name in self.TRAVERSE_AND_IGNORE_TAGS:
                    return self.traverse_html_tag(tag.contents)
                if tag.name in self.IGNORE_TAGS:
                    return
            else:
                value = klass(self.traverse_html_tag(tag.contents))
                return HTMLPDFFieldElementList(value)

            error_msg = ('"%s" is not an accepted HTML tag in '
                         '"traverse_html_tag()" method. Skipped.')
            logger.error(error_msg, tag.name)
            raise HTMLPDFFieldElementNotFound
