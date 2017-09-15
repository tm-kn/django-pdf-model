(WORK IN PROGRESS) django-pdf-model
===================================
Generate PDFs out of Django models.

Features worked on
******************
* Django model's support
* Basic ReportLab support
* Wagtail support
* Wagtail's StreamField support
* Add structured content, e.g. chapters etc.

Usage with Django
*****************

#. Specify your model that subclasses from `PDFModelMixin` and defines `pdf_field_list`.

   .. code:: python

       from django.conf import settings
       from django.db import models

       from django_pdf.models import PDFModelMixin


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

#. Add a URL entry for the view.

   .. code:: python

       from django.conf.urls import url

       from .models import Report


       urlpatterns = [
           url(r'^report-pdf/(?P<pk>[\d]+)/$', Report.as_pdf_view()),
       ]
