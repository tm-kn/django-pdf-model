from numbers import Number

from .exceptions import PDFFieldCleaningError


class PDFField(object):
    ALLOWED_VALUE_TYPES = []

    def __init__(self, name, **kwargs):
        self.name = name

    def clean(self, value, context=None):
        if not isinstance(value, self.get_allowed_value_types()):
            raise PDFFieldCleaningError(
                '"value" is of type {} which is not allowed for {}. Only {} '
                'accpeted.'.format(type(value).__name__,
                                   self.__class__.__name__,
                                   ','.join(self.get_allowed_value_types())))

        return self._clean_value(value, context=context)

    def _clean_value(self, value, context=None):
        not_implemented_error = '{class_name} must implement the ' \
                                '_clean_value() method.'

        raise NotImplementedError(
                not_implemented_error.format(class_name=self.__class__.__name)
        )

    @classmethod
    def get_allowed_value_types(cls):
        return tuple(cls.ALLOWED_VALUE_TYPES)


class CharPDFField(PDFField):
    ALLOWED_VALUE_TYPES = [str, Number]

    def _clean_value(self, value, context=None):
        # If it's number or string, just make sure it
        # returns string.
        return str(value)


class TitlePDFField(CharPDFField):
    pass


class PDFFieldBoundValue(object):
    """
    Container binding PDFField and associated value.
    """
    def __init__(self, field, value):
        if not isinstance(field, PDFField):
            raise TypeError('"field" has to be a PDFField instance.')

        self.field = field

        if not isinstance(value, field.get_allowed_value_types()):
            raise TypeError('"value" must be {}'.format(
                ','.join(field.get_allowed_value_types())
            ))

        self.value = value
