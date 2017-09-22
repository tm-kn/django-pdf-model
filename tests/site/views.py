from django.http import HttpResponse

from .models import Report


def report_list_view(request):
    html_elements = []

    for report in Report.objects.all():
        html_elements.append('<li><a href="{url}">{name}</a></li>'.format(
            url=report.get_absolute_url(),
            name=report.title
        ))

    html = '<html><body><ul>{}</ul></body></html>'

    return HttpResponse(html.format(''.join(html_elements)))
