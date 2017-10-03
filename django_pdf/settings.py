from django.conf import settings

__pdf_renderer_class = '{package}.reportlab.renderers' \
                       '.SimpleDocTemplateReportLabPDFRenderer'

__pdf_model_cleaner_class = '{package}.cleaners.PDFModelCleaner'

__model_to_pdf_handler_class = '{package}.handlers.ModelToPDFHandler'

PDF_RENDERER_CLASS = getattr(
    settings,
    'PDF_RENDERER_CLASS',
    __pdf_renderer_class.format(package=__package__)
)

PDF_MODEL_CLEANER_CLASS = getattr(
    settings,
    'PDF_MODEL_CLEANER',
    __pdf_model_cleaner_class.format(package=__package__)
)

MODEL_TO_PDF_HANDLER_CLASS = getattr(
    settings,
    'MODEL_TO_PDF_HANDLER_CLASS',
    __model_to_pdf_handler_class.format(package=__package__)
)
