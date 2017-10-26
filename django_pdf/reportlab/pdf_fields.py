from reportlab.platypus import Flowable

from django_pdf.pdf_fields import AbstractPDFField


class ReportLabFlowablePDFField(AbstractPDFField):
    ALLOWED_VALUE_TYPES = [object]

    def __init__(self, name, flowable_class=None, **kwargs):
        if not flowable_class:
            raise ValueError(
                '"flowable_class" kwarg cannot be empty on {}.'.format(
                    self.__class__.__name__
                )
            )
        if not issubclass(flowable_class, Flowable):
            raise TypeError(
                '"flowable_class" kwarg\'s value has to be the ReportLab\'s '
                'Flowable class.'.format(
                    self.__class__.__name__
                )
            )
        super().__init__(name, **kwargs)

    def clean_value(self, value, context=None):
        # Not doing any validation - it can be done inside the Flowable
        return value
