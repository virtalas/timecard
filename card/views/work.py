from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from datetime import datetime, date, timedelta
from django.utils import timezone
from ..models import Project, Work, Minutes

from django.contrib.auth.decorators import login_required


@login_required(login_url='/timecard/login')
def start_new_work(request, project_id):
    # Get start time from GET-parameters
    start_hour = int(request.GET.get("start_hour"))
    start_minute = int(request.GET.get("start_minute"))
    start_time = datetime.now().replace(hour=start_hour, minute=start_minute)
    # start_time = timezone.localtime(start_time)

    project = get_object_or_404(Project, pk=project_id)
    # Start timers only for active projects
    if (project.end_date is None):
        user_id = request.user.id
        project.work_set.create(user_id=user_id, start_time=start_time)
    return HttpResponseRedirect(reverse('card:index'))

@login_required(login_url='/timecard/login')
def done(request, work_id):
    work = get_object_or_404(Work, pk=work_id)
    work.end_time = timezone.now()
    work.save()
    return HttpResponseRedirect(reverse('card:index'))

@login_required(login_url='/timecard/login')
def done_for_today(request, work_id):
    user_id = request.user.id
    work = get_object_or_404(Work, pk=work_id)
    today = date.today()
    todays_work = Work.objects.filter(end_time__isnull=False, start_time__year=today.year, start_time__month=today.month, start_time__day=today.day, user_id=user_id)
    minutes_per_day = Minutes.objects.current_minutes_per_day(user_id)
    seconds_of_work = 0

    for w in todays_work:
        seconds_of_work += w.seconds_of_work()

    minutes_of_work = int(seconds_of_work / 60)
    minutes_left_for_today = minutes_per_day - minutes_of_work

    # Is today's balance positive or negative
    if minutes_left_for_today < 0:
        # Negative, don't do anything
        return HttpResponseRedirect(reverse('card:index'))

    # Set the stop time for the current work so that balance for today becomes 0
    end_time = work.start_time + timedelta(minutes=minutes_left_for_today)

    work.end_time = end_time
    work.save()

    return HttpResponseRedirect(reverse('card:index'))

@login_required(login_url='/timecard/login')
def add(request):
    user_id = request.user.id
    active_projects = Project.objects.order_by('name').filter(end_date__isnull=True, user_id=user_id)
    return render(request, 'card/work/add.html', {"projects": active_projects})

@login_required(login_url='/timecard/login')
def add_new_work(request):
    user_id = request.user.id
    project_id = request.POST['project_id']
    start_time = request.POST['start_time']
    end_time = request.POST['end_time']

    try:
        work = Work(project_id=project_id, user_id=user_id, start_time=start_time, end_time=end_time)
        work.save()
        return HttpResponseRedirect(reverse('card:history'))
    except:
        active_projects = Project.objects.order_by('name').filter(end_date__isnull=True, user_id=user_id)

        context = {
            "projects": active_projects,
            "error": "Date was given incorrectly.",
            "start_time": start_time,
            "end_time": end_time,
            "project_id": int(project_id)
        }

        return render(request, 'card/work/add.html', context)

@login_required(login_url='/timecard/login')
def edit(request, work_id):
    work = get_object_or_404(Work, pk=work_id)
    user_id = request.user.id
    active_projects = Project.objects.order_by('name').filter(end_date__isnull=True, user_id=user_id)

    context = {
        "projects": active_projects,
        "start_time": work.start_time,
        "end_time": work.end_time,
        "project_id": work.project_id,
        "work_id": work.id
    }

    return render(request, 'card/work/edit.html', context)

@login_required(login_url='/timecard/login')
def update(request, work_id):
    user_id = request.user.id
    work = get_object_or_404(Work, pk=work_id)
    project_id = request.POST['project_id']
    start_time = request.POST['start_time']
    end_time = request.POST['end_time']

    try:
        work.project_id = project_id
        work.start_time = start_time
        work.end_time = end_time
        work.save()
        return HttpResponseRedirect(reverse('card:history'))
    except:
        active_projects = Project.objects.order_by('name').filter(end_date__isnull=True, user_id=user_id)

        context = {
            "error": "Date was given incorrectly.",
            "projects": active_projects,
            "start_time": start_time,
            "end_time": end_time,
            "project_id": int(project_id),
            "work_id": work_id
        }

        return render(request, 'card/work/edit.html', context)

@login_required(login_url='/timecard/login')
def delete(request, work_id):
    work = get_object_or_404(Work, pk=work_id)
    work.delete()
    return HttpResponseRedirect(reverse('card:history'))
