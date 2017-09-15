from django_pdf.views import PDFModelView

from .models import Report


class ReportPDFModelView(PDFModelView):
    model = Report
