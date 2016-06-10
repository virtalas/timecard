from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from ..models import Project, Work, Minutes

import datetime

from django.contrib.auth.decorators import login_required


@login_required(login_url='/card/login')
def index(request):
    user_id = request.user.id
    all_work = Work.objects.filter(end_time__isnull=False, user_id=user_id)
    work_days = minutes_of_work_per_day(all_work)
    hours = total_balance_hours(all_work, user_id, work_days)

    context = {
        'total_balance': hours
    }

    return render(request, 'card/balance/index.html', context)

@login_required(login_url='/card/login')
def report(request):
    user_id = request.user.id
    all_work = Work.objects.filter(end_time__isnull=False, user_id=user_id).order_by('start_time')
    work_days_minutes = minutes_of_work_per_day(all_work)
    hours = total_balance_hours(all_work, user_id, work_days_minutes)

    start_date = datetime.datetime.strptime(request.POST['start_d'], '%Y-%m-%d')
    end_date = datetime.datetime.strptime(request.POST['end_d'], '%Y-%m-%d')
    selected_work = all_work.filter(start_time__gte=start_date, start_time__lt=end_date + datetime.timedelta(days=1))

    work_days_information = {}
    project_minutes = {}

    for work in selected_work:
        work_date = "" + str(work.start_time.year) + "-" + str(work.start_time.month) + "-" + str(work.start_time.day)
        minutes_of_work = work.seconds_of_work() / 60
        formatted_work = {
            "project": work.project.name,
            "start_time": work.start_time,
            "end_time": work.end_time,
            "minutes_of_work": minutes_of_work
        }

        # Store work in a dict with the date as key, and each date has a list of work-dicts.
        if work_date in work_days_information:
            work_days_information[work_date].append(formatted_work)
        else:
            work_days_information[work_date] = [formatted_work]

        # Keep track of minutes per project
        if str(work.project_id) in project_minutes:
            project_minutes[str(work.project_id)]['minutes_of_work'] += minutes_of_work
        else:
            project_minutes[str(work.project_id)] = {
                "name": work.project.name,
                "minutes_of_work": minutes_of_work
            }

    context = {
        'report': True,
        'total_balance': hours,
        'start_date': request.POST['start_d'],
        'end_date': request.POST['end_d'],
        'work_days_information': work_days_information,
        'work_days_minutes': work_days_minutes,
        'minutes_per_day': Minutes.objects.minutes_per_day(user_id),
        'project_minutes': project_minutes
    }

    return render(request, 'card/balance/index.html', context)

def minutes_of_work_per_day(all_work):
    work_days = {}

    for work in all_work:
        work_date = "" + str(work.start_time.year) + "-" + str(work.start_time.month) + "-" + str(work.start_time.day)
        minutes_of_work = work.seconds_of_work() / 60

        # Store minutes of work per day in a dict with date as key
        if work_date in work_days:
            work_days[work_date] += minutes_of_work
        else:
            work_days[work_date] = minutes_of_work

    return work_days

def total_balance_hours(all_work, user_id, work_days):
    total_balance_minutes = 0

    minutes_per_day = Minutes.objects.minutes_per_day(user_id)
    hours_per_day = Minutes.objects.hours_per_day(user_id)

    for date, minutes_of_work in work_days.iteritems():
        total_balance_minutes += minutes_of_work - minutes_per_day

    hours = round(total_balance_minutes / 60, 1)
    return hours
