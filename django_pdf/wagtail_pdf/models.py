from wagtail.wagtailcore.models import Page
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route

from ..models import PDFModelMixin


class PDFPageMixin(PDFModelMixin, RoutablePageMixin, Page):
    class Meta:
        abstract = True

    @route('^pdf/$', name='pdf')
    def pdf_view(self, request):
        pass
