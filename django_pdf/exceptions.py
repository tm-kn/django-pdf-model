class PDFFieldError(Exception):
    pass


class PDFFieldCleaningError(PDFFieldError):
    pass


class PDFFieldConfigurationError(PDFFieldError):
    pass


class PDFRendererError(Exception):
    pass


class PDFFieldRendererError(Exception):
    pass


class PDFFieldRendererNotFound(PDFFieldRendererError):
    pass


class PDFFieldRendererConfigurationError(PDFFieldRendererError):
    pass
