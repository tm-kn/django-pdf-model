class PDFFieldError(Exception):
    pass


class PDFFieldCleaningError(PDFFieldError):
    pass


class PDFFieldConfigurationError(PDFFieldError):
    pass


class HTMLPDFFieldElementNotFound(Exception):
    pass


class PDFFieldRendererError(Exception):
    pass


class PDFFieldRendererNotFound(PDFFieldRendererError):
    pass


class PDFFieldRendererConfigurationError(PDFFieldRendererError):
    pass
