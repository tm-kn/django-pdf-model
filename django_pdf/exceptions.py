class PDFFieldError(Exception):
    pass


class PDFFieldCleaningError(PDFFieldError):
    pass


class PDFFieldConfigurationError(PDFFieldError):
    pass
