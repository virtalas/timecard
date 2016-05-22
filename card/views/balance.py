from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from django.utils import timezone
import time
from ..models import Project, Work, User

def index(request):
    # user id = 2 until logging in implemented
    user_id = 2
    all_work = Work.objects.filter(end_time__isnull=False, user_id=user_id)
    work_days = {}

    for work in all_work:
        work_date = "" + str(work.start_time.year) + "-" + str(work.start_time.month) + "-" + str(work.start_time.day)

        d1_ts = time.mktime(work.start_time.timetuple())
        d2_ts = time.mktime(work.end_time.timetuple())
        minutes_of_work = int(d2_ts - d1_ts) / 60

        # Store minutes of work per day in a dict with date as key
        if work_date in work_days:
            work_days[work_date] += minutes_of_work
        else:
            work_days[work_date] = minutes_of_work

    print(work_days)

    total_balance_minutes = 0
    # user's own hours_per_day
    hours_per_day = 7.4
    minutes_per_day = hours_per_day * 60

    for date, minutes_of_work in work_days.iteritems():
        total_balance_minutes += minutes_of_work - minutes_per_day

    total_balance_hours = round(total_balance_minutes / 60, 1)

    context = {
        'total_balance': total_balance_hours
    }

    return render(request, 'card/balance/index.html', context)
