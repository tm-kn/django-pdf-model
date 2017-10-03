from numbers import Number

from . import PDFField


class CharPDFField(PDFField):
    ALLOWED_VALUE_TYPES = [str, Number]

    def clean_value(self, value, context=None):
        # If it's number or string, just make sure it
        # returns string.
        return str(value)


class TitlePDFField(CharPDFField):
    pass


class ParagraphPDFField(CharPDFField):
    pass


class HeadingPDFField(CharPDFField):
    HEADINGS_RANGE = list(range(1, 7))

    def __init__(self, name, heading_level=1, **kwargs):
        super().__init__(name, **kwargs)

        if int(heading_level) not in self.HEADINGS_RANGE:
            error_msg = '"heading_level" has to be in range from {from} to ' \
                        '{to}.'
            raise ValueError(error_msg.format(self.HEADINGS_RANGE[0],
                                              self.HEADINGS_RANGE[-1]))

        self.heading_level = heading_level
