from django.conf.urls import url

from .models import Report


urlpatterns = [
    url(r'^report-pdf/(?P<pk>[\d]+)/$', Report.as_pdf_view()),
]
