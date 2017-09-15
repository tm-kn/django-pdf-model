from django.conf import settings
from django.db import models
from django_pdf.models import PDFModelMixin
from django_pdf import pdf_fields


class Report(PDFModelMixin, models.Model):
    title = models.CharField(max_length=255)
    introduction = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.PROTECT)

    pdf_field_list = [
        pdf_fields.TitlePDFField('title'),
        pdf_fields.TitlePDFField('introduction'),
        pdf_fields.TitlePDFField('content'),
        pdf_fields.TitlePDFField('author_name'),
    ]

    @property
    def author_name(self):
        return self.author.get_full_name()
