from django.test import TestCase

from .models import Report


class TestReport(TestCase):
    def test_sample_report_does_not_crash(self):
        report = Report.objects.first()
        response = self.client.get(report.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
