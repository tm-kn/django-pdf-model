from django.shortcuts import render

from .models import Report


def report_list_view(request):
    context = {
        'reports': Report.objects.all()
    }

    return render(request, 'report_list.html', context)
