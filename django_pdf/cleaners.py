import logging

from django.utils.functional import cached_property

from .exceptions import PDFFieldConfigurationError, PDFFieldError
from .pdf_fields import AbstractPDFField, PDFFieldBoundValue


logger = logging.getLogger(__name__)


class PDFModelCleaner(object):
    def __init__(self, instance, fields=None, context=None):
        if fields is None:
            fields = instance.get_pdf_fields()

        # Set fields
        try:
            for field in fields:
                if not isinstance(field, AbstractPDFField):
                    raise TypeError('"field" has to be an AbstractPDFField '
                                    'instance.')
        except TypeError:
            raise TypeError('"fields" has to be a list of AbstractPDFField '
                            'instances.')

        self.fields = fields

        # Set instance
        if not isinstance(instance, object):
            raise TypeError('"instance" should be an object.')

        self.instance = instance

        # Set context
        if context is None:
            context = {}

        if not isinstance(context, dict):
            raise TypeError("\"context\" has to be a dictionary.")

        self.context = context

    def clean(self):
        try:
            del self.cleaned_data
        except AttributeError:
            pass

        return self.cleaned_data

    def _get_cleaned_data(self):
        for bound_value in self._get_values():
            yield (bound_value.field.name, bound_value)

    @cached_property
    def cleaned_data(self):
        return list(self._get_cleaned_data())

    def _clean_field(self, field, value):
        return field.clean(value, context=self.context)

    def _get_instance_attribute_value(self, attribute_name):
        instance_value = getattr(self.instance, attribute_name)

        if callable(instance_value):
            instance_value = instance_value()

        return instance_value

    def _get_value_for_field(self, field):
        if not hasattr(self.instance, field.name):
            error_msg = "\"{attribute}\" is not an attribute on {model}."

            raise PDFFieldConfigurationError(error_msg.format(
                attribute=field.name,
                model=self.instance.__class__.__name__)
            )

        instance_value = self._get_instance_attribute_value(field.name)

        if instance_value is None:
            return

        cleaned_value = self._clean_field(field, instance_value)

        return PDFFieldBoundValue(field, cleaned_value)

    def _get_values(self):
        for field in self.fields:
            try:
                field_value = self._get_value_for_field(field)
            except PDFFieldError:
                logger.exception("Error when trying to get field's value.")
            else:
                if field_value:
                    yield field_value
