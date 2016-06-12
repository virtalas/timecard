from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from datetime import date
import time
from django.utils import timezone
from ..models import Project, Work, Minutes

from django.contrib.auth.decorators import login_required


def index(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        active_projects = Project.objects.order_by('name').filter(end_date__isnull=True, user_id=user_id)
        current_work_list = Work.objects.filter(end_time__isnull=True, user_id=user_id)
        current_work = None

        seconds_of_work = 0

        # There is a currently active timer
        if current_work_list:
            current_work = current_work_list[0]
            # Work from the current work up to this point in time
            d1_ts = time.mktime(current_work.start_time.timetuple())
            d2_ts = time.mktime(timezone.now().timetuple())
            seconds_of_work += d2_ts - d1_ts

        today = date.today()
        todays_work = Work.objects.filter(end_time__isnull=False, start_time__year=today.year, start_time__month=today.month, start_time__day=today.day, user_id=user_id)

        for work in todays_work:
            seconds_of_work += work.seconds_of_work()

        minutes_of_work = int(seconds_of_work / 60)
        minutes_per_day = Minutes.objects.current_minutes_per_day(user_id)

        # Is today's balance positive or negative
        if minutes_per_day - minutes_of_work < 0:
            negative = True
        else:
            negative = False

        total_minutes_left = abs(minutes_per_day - minutes_of_work)
        hours_left = int(total_minutes_left / 60)
        minutes_left = int(total_minutes_left - hours_left * 60)

        context = {
            'projects': active_projects,
            'current_work': current_work,
            'todays_work': todays_work,
            'hours_left': hours_left,
            'minutes_left': minutes_left,
            "negative": negative
        }

        return render(request, 'card/index.html', context)
    else:
        return render(request, 'card/index.html')
