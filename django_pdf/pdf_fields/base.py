from ..exceptions import PDFFieldCleaningError


class AbstractPDFField(object):
    ALLOWED_VALUE_TYPES = []

    def __init__(self, name, **kwargs):
        self.name = name
        self.kwargs = kwargs

    def clean(self, value, context=None):
        if not isinstance(value, self.get_allowed_value_types()):
            raise PDFFieldCleaningError(
                '"value" is of type {} which is not allowed for {}. Only {} '
                'accpeted.'.format(type(value).__name__,
                                   self.__class__.__name__,
                                   ','.join(self.get_allowed_value_types())))

        return self.clean_value(value, context=context)

    def clean_value(self, value, context=None):
        not_implemented_error = '{class_name} must implement the ' \
                                'clean_value() method.'

        raise NotImplementedError(
                not_implemented_error.format(class_name=self.__class__.__name)
        )

    @classmethod
    def get_allowed_value_types(cls):
        return tuple(cls.ALLOWED_VALUE_TYPES)


class PDFFieldBoundValue(object):
    """
    Container binding PDFField and associated value.
    """
    def __init__(self, field, value):
        if not isinstance(field, AbstractPDFField):
            raise TypeError('"field" has to be an AbstractPDFField instance.')

        self.field = field
        self.value = value
