from django.conf import settings

__pdf_renderer_class = '{package}.reportlab.renderers' \
                       '.SimpleDocTemplateReportLabPDFRenderer'

PDF_RENDERER_CLASS = getattr(settings, 'PDF_RENDERER_CLASS',
                             __pdf_renderer_class.format(package=__package__))
