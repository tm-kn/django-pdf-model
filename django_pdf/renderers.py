import logging

from .exceptions import (
    PDFFieldRendererConfigurationError,
    PDFFieldRendererNotFound
)
from .pdf_fields import PDFField


logger = logging.getLogger(__name__)


class PDFFieldRenderer(object):
    field_type = None

    def __init__(self):
        if not hasattr(self, 'field_type') \
                or self.field_type is PDFField \
                or not issubclass(self.field_type, PDFField):
            raise PDFFieldRendererConfigurationError(
                '{}.field_type has to be a PDFField subclass"'.format(
                    self.__class__.__name__
                )
            )

    def render(self, pdf_renderer, field_bound_value):
        raise NotImplementedError("PDFFieldRenderer has to implement "
                                  "render() method.")


class PDFRenderer(object):
    def __init__(self, buffer_object, context=None):
        self.buffer_object = buffer_object
        self.set_up()

        if context is None:
            context = {}

        if not isinstance(context, dict):
            raise TypeError("context has to be a dictionary.")

        self.context = context

    def set_up(self):
        raise NotImplementedError("PDFRenderer has to implement "
                                  "set_up() method.")

    def render_field(self, field_bound_value):
        try:
            renderer_class = self._find_field_renderer(field_bound_value.field)
        except PDFFieldRendererNotFound:
            error_msg = "Could not find a field renderer for field type " \
                        "%(field)s"
            logger.excetion(error_msg,
                            field=field_bound_value.__class__.__name__)
        else:
            field_renderer = renderer_class()
            field_renderer.render(self, field_bound_value)

    def save(self):
        raise NotImplementedError("PDFRenderer has to implement "
                                  "save() method.")

    def _get_field_renderers(self):
        field_dictionary = {}

        for field_renderer in self.field_renderers:
            field_dictionary[field_renderer.field_type] = field_renderer

        return field_dictionary

    def _find_field_renderer(self, field):
        """ Find field renderer for a specific PDFField class. """
        field_renderers = self._get_field_renderers()

        # Go through all the base classes of the field and find the
        # closest one that has render specified.
        iterator = iter(field.__class__.mro())
        field_class = next(iterator)

        while field_class is not PDFField:
            try:
                return field_renderers[field_class]
            except KeyError:
                pass

            field_class = next(iterator)

        raise PDFFieldRendererNotFound
