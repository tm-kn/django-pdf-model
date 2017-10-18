from django.conf import settings
from django.db import models
from django.shortcuts import reverse

from django_pdf.models import PDFModelMixin
from django_pdf import pdf_fields


class Report(PDFModelMixin, models.Model):
    title = models.CharField(max_length=255)
    introduction = models.CharField(max_length=255)
    content = models.TextField()
    html_content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.PROTECT)

    pdf_field_list = [
        pdf_fields.TitlePDFField('title'),
        pdf_fields.HeadingPDFField('introduction', heading_level=3),
        pdf_fields.CharPDFField('content'),
        pdf_fields.CharPDFField('author_name'),
        pdf_fields.HTMLPDFField('html_content'),
        pdf_fields.HTMLPDFField('some_html_content'),
    ]

    @property
    def author_name(self):
        return self.author.get_full_name()

    def some_html_content(self):
        return """
        <p>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        Nulla ut vestibulum lectus, ac pharetra lectus. Mauris hendrerit
        purus sapien, ac egestas ipsum aliquam vitae.
        </p>
        <u>Pellentesque porta
        varius eros. Sed at tincidunt nisl. Phasellus turpis lectus,
        aliquam sed facilisis et, dignissim et sem.</u>
        <strong>Sed venenatisconsectetur tellus, non rhoncus lorem scelerisque
        ut. Praesent diam orci, porttitor vel cursus quis, accumsan sed risus.
        Ut commodo, ex id ultrices pretium, eros nunc scelerisque risus, et
        sodales justo erat id risus. Nulla at condimentum elit.</strong>
        """

    def get_absolute_url(self):
        return reverse('report-pdf', args=[str(self.pk)])

    def __str__(self):
        return self.title
