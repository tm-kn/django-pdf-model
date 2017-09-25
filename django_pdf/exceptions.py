class PDFFieldError(Exception):
    pass


class PDFFieldCleaningError(PDFFieldError):
    pass


class PDFFieldConfigurationError(PDFFieldError):
    pass


class PDFRendererError(Exception):
    pass
