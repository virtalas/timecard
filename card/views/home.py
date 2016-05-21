from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from datetime import date
from django.utils import timezone
from ..models import Project, Work, User


def index(request):
    projects = Project.objects.order_by('-name')
    current_work_list = Work.objects.filter(end_time__isnull=True)
    current_work = None
    if current_work_list:
        current_work = current_work_list[0]

    today = date.today()
    todays_work = Work.objects.filter(start_time__year=today.year, start_time__month=today.month, start_time__day=today.day)

    print(todays_work)

    context = {
        'projects': projects,
        'current_work': current_work,
        'todays_work': todays_work
    }

    return render(request, 'card/index.html', context)
