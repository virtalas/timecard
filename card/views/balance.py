from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from ..models import Project, Work, Minutes

from django.contrib.auth.decorators import login_required


@login_required(login_url='/card/login')
def index(request):
    user_id = request.user.id
    all_work = Work.objects.filter(end_time__isnull=False, user_id=user_id)
    work_days = {}

    for work in all_work:
        work_date = "" + str(work.start_time.year) + "-" + str(work.start_time.month) + "-" + str(work.start_time.day)

        minutes_of_work = work.seconds_of_work() / 60

        # Store minutes of work per day in a dict with date as key
        if work_date in work_days:
            work_days[work_date] += minutes_of_work
        else:
            work_days[work_date] = minutes_of_work

    print(work_days)

    total_balance_minutes = 0

    minutes_per_day = Minutes.objects.minutes_per_day(user_id)
    hours_per_day = Minutes.objects.hours_per_day(user_id)

    for date, minutes_of_work in work_days.iteritems():
        total_balance_minutes += minutes_of_work - minutes_per_day

    total_balance_hours = round(total_balance_minutes / 60, 1)

    context = {
        'total_balance': total_balance_hours
    }

    return render(request, 'card/balance/index.html', context)
