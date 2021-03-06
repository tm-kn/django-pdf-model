import logging
from urllib.parse import urlparse

from bs4 import BeautifulSoup, NavigableString, Tag

from . import AbstractPDFField
from ..exceptions import HTMLPDFFieldElementNotFound, PDFFieldCleaningError

logger = logging.getLogger(__name__)


class HTMLPDFFieldElement(object):
    def __init__(self, value, **kwargs):
        self.value = value
        self.attrs = {}
        # Get HTML attributes attributes required by the field
        if isinstance(kwargs.get('attrs'), dict):
            self.attrs = kwargs['attrs']
        if self.attrs is not None and not isinstance(self.attrs, dict):
            raise TypeError('"attrs" has to be a dicitonary or None.')
        if self.get_required_attrs():
            for req_attr in self.get_required_attrs():
                if req_attr not in self.attrs:
                    raise PDFFieldCleaningError(f'"{req_attr}" has to be '
                                                'passed to '
                                                f'{type(self).__name__}.')

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.value)})"

    @classmethod
    def get_required_attrs(cls):
        if hasattr(cls, 'REQUIRED_ATTRS'):
            return cls.REQUIRED_ATTRS
        return {}

    def clean(self, context):
        pass


class HTMLPDFFieldElementList(list):
    def __init__(self, *args):
        super().__init__()
        for arg in args:
            self.append(arg)

    def append(self, value):
        if not isinstance(value, HTMLPDFFieldElement):
            raise TypeError(f"{type(self).__name__} has to contain "
                            "HTMLPDFFieldElement objects only, "
                            f"not {type(value)}.")
        super().append(value)

    def __repr__(self):
        return f"{type(self).__name__}({super().__repr__()})"


class HTMLPDFFieldText(HTMLPDFFieldElement):
    pass


class HTMLPDFFieldParagraph(HTMLPDFFieldElement):
    pass


class HTMLPDFFieldImage(HTMLPDFFieldElement):
    REQUIRED_ATTRS = ['src']


class HTMLPDFFieldUnorderedList(HTMLPDFFieldElement):
    pass


class HTMLPDFFieldOrderedList(HTMLPDFFieldElement):
    pass


class HTMLPDFFieldListItem(HTMLPDFFieldElement):
    pass


class HTMLPDFFieldAnchor(HTMLPDFFieldElement):
    REQUIRED_ATTRS = ['href']

    def clean(self, context):
        # If the URL is already absolute, let's leave it that way
        location = self.attrs['href']
        is_absolute = bool(urlparse(location).netloc)
        if is_absolute:
            return
        # Build absolute URL
        request = context.get('request')
        if request and hasattr(request, 'build_absolute_uri'):
            request.build_absolute_uri(location)
            self.attrs['href'] = request.build_absolute_uri(location)
            return
        # Delete href if we can't build absolute URL
        self.attrs['href'] = ''

    def get_url(self):
        return self.attrs['href']


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
    Image = HTMLPDFFieldImage
    ItalicText = HtmlPDFFieldItalicText
    ListItem = HTMLPDFFieldListItem
    OrderedList = HTMLPDFFieldOrderedList
    Paragraph = HTMLPDFFieldParagraph
    StrikeThroughText = HtmlPDFFieldStrikeThroughText
    Text = HTMLPDFFieldText
    UnderlinedText = HtmlPDFFieldUnderlinedText
    UnorderedList = HTMLPDFFieldUnorderedList
    NewLine = HtmlPDFFieldNewLine
    HTML_TAG_MAPPINGS = {
        'a': Anchor,
        ('b', 'strong'): BoldText,
        'br': NewLine,
        ('del', 's', 'strike'): StrikeThroughText,
        ('i', 'em'): ItalicText,
        'img': Image,
        'li': ListItem,
        'ol': OrderedList,
        'p': Paragraph,
        'u': UnderlinedText,
        'ul': UnorderedList,
    }
    TRAVERSE_AND_IGNORE_TAGS = [
        'body',
        'div',
        'html',
    ]
    IGNORE_TAGS = [
        'embed',
        'head',
        'iframe',
        'script',
        'style',
    ]

    def clean_value(self, value, context=None):
        return self.convert_html_to_pdf_field_structure(value, context)

    def convert_html_to_pdf_field_structure(self, value, context):
        soup = BeautifulSoup(value, 'html5lib')
        try:
            return self.traverse_html_tag(soup.body.contents, context)
        except HTMLPDFFieldElementNotFound:
            logger.exception("Could not find any HTML elements to generate "
                             "PDF content out of.")

    def convert_html_to_pdf_text(self, value, context):
        value = str(value)
        html_list = HTMLPDFFieldElementList()
        # Convert new line characters
        splitlined_string = value.splitlines()
        for key, text_string in enumerate(splitlined_string):
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

    def traverse_list(self, tags_list, context):
        structure = HTMLPDFFieldElementList()
        for child in tags_list:
            try:
                structure += self.traverse_html_tag(child, context)
            except HTMLPDFFieldElementNotFound:
                logger.exception('Could not generate PDF content out of the '
                                 'HTML content.')
        return structure

    def traverse_tag_instance(self, tag, context):
        try:
            klass = self.get_pdf_field_element_for_tag(tag.name)
        except KeyError:
            if tag.name in self.TRAVERSE_AND_IGNORE_TAGS:
                return self.traverse_html_tag(tag.contents, context)
            if tag.name in self.IGNORE_TAGS:
                return HTMLPDFFieldElementList()
        else:
            # Get required attributes from the tag
            attrs = {req_attr: tag.attrs.get(req_attr)
                     for req_attr in klass.get_required_attrs()}
            try:
                value = klass(self.traverse_html_tag(tag.contents, context),
                              attrs=attrs)
                value.clean(context)
            except PDFFieldCleaningError:
                logger.exception("Cleaning error when traversing HTML "
                                 "structure.")
                return HTMLPDFFieldElementList()
            return HTMLPDFFieldElementList(value)

        error_msg = ('"%s" is not an accepted HTML tag in '
                     '"traverse_html_tag()" method. Skipped.')
        logger.error(error_msg, tag.name)
        raise HTMLPDFFieldElementNotFound

    def traverse_html_tag(self, tag, context):
        # If it's a list, evaluate its children and append
        if isinstance(tag, list):
            return self.traverse_list(tag, context)
        # Convert strings to PDF field text object.
        if isinstance(tag, NavigableString):
            return self.convert_html_to_pdf_text(str(tag), context)
        # Convert tag to a PDF field type and evaluate its children.
        if isinstance(tag, Tag):
            return self.traverse_tag_instance(tag, context)
