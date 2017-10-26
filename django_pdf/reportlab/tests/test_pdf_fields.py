from django.test import TestCase

from reportlab.platypus import Flowable

from django_pdf.reportlab.pdf_fields import ReportLabFlowablePDFField


class TestReportLabFlowablePDFField(TestCase):
    def test_init_without_flowable(self):
        with self.assertRaises(ValueError) as cm:
            ReportLabFlowablePDFField('some_name')
        self.assertEqual(str(cm.exception),
                         '"flowable_class" kwarg cannot be empty on '
                         'ReportLabFlowablePDFField.')

    def test_init_with_wrong_flowable_type(self):
        with self.assertRaises(TypeError) as cm:
            ReportLabFlowablePDFField('some_name', flowable_class=list)
        self.assertEqual(str(cm.exception),
                         '"flowable_class" kwarg\'s value has to be the '
                         'ReportLab\'s Flowable class.')

    def test_init_with_flowable_type(self):
        ReportLabFlowablePDFField('some_name', flowable_class=Flowable)

    def test_clean(self):
        field = ReportLabFlowablePDFField('some_name', flowable_class=Flowable)
        self.assertEqual(field.clean('Lorem ipsum'), 'Lorem ipsum')
        self.assertEqual(field.clean(['123', '123123']), ['123', '123123'])
        some_object = object()
        self.assertIs(field.clean(some_object), some_object)
