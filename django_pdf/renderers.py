class PDFRenderer(object):
    def __init__(self, buffer_object):
        self.buffer_object = buffer_object
        self.set_up()

    def set_up(self):
        raise NotImplementedError("PDFRenderer has to implement "
                                  "set_up() method.")

    def render_field(self, field_bound_value):
        raise NotImplementedError("PDFRenderer has to implement "
                                  "render_field() method.")

    def save(self):
        raise NotImplementedError("PDFRenderer has to implement "
                                  "save() method.")
