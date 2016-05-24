from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from datetime import date
import time
from django.utils import timezone
from ..models import Project, Work, User

from django.contrib.auth.decorators import login_required


def index(request):
    if request.user.is_authenticated():
        # user id = 2 until logging in implemented
        user_id = 2
        active_projects = Project.objects.order_by('-name').filter(end_date__isnull=True, user_id=2)
        current_work_list = Work.objects.filter(end_time__isnull=True, user_id=user_id)
        current_work = None

        minutes_of_work = 0

        # There is a currently active timer
        if current_work_list:
            current_work = current_work_list[0]
            # Work from the current work up to this point in time
            d1_ts = time.mktime(current_work.start_time.timetuple())
            d2_ts = time.mktime(timezone.now().timetuple())
            minutes_of_work += int(d2_ts - d1_ts) / 60

        today = date.today()
        todays_work = Work.objects.filter(end_time__isnull=False, start_time__year=today.year, start_time__month=today.month, start_time__day=today.day, user_id=user_id)

        for work in todays_work:
            d1_ts = time.mktime(work.start_time.timetuple())
            d2_ts = time.mktime(work.end_time.timetuple())
            minutes_of_work += int(d2_ts - d1_ts) / 60

        # use user's own hours_per_day here
        hours_per_day = 7.4
        minutes_per_day = hours_per_day * 60

        total_minutes_left = minutes_per_day - minutes_of_work
        hours_left = int(total_minutes_left / 60)
        minutes_left = int(total_minutes_left - hours_left * 60)

        context = {
            'projects': active_projects,
            'current_work': current_work,
            'todays_work': todays_work,
            'hours_left': hours_left,
            'minutes_left': minutes_left
        }

        return render(request, 'card/index.html', context)
    else:
        return render(request, 'card/index.html')
