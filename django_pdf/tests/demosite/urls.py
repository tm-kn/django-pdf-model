from django.conf.urls import url

from .models import Report
from .views import report_list_view


urlpatterns = [
    url(r'^$', report_list_view, name='report-list'),
    url(r'^report-pdf/(?P<pk>[\d]+)/$', Report.as_pdf_view(),
        name='report-pdf'),
]
